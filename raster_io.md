# Reading remote sensing images into Python and R

> This guide assumes you have
and Anaconda environment set up with `rasterio`, `rsgislib` and `rios`, and that
you have ran the necessary setup scripts to download the example data. See the
[setup](setup.md) section for details.

There are two main "philosophies" of
working with remote sensing images using scripts, which we will call here LOADED
and UNLOADED **USE BETTER NAMES LATER**. The UNLOADED way is to simply pass on
the file name for an image that exists on disk. The function will then do what
it is supposed to do with the file, and save the output if applicable, but the
image never becomes a variable/object that can be acessesed by other Python or R
functions within your working session.

This is usually the `RSGISlib` way. Let
say we are writing a Python script to subset an image using a polygon shapefile:

```python
# First step is to import the rsgislib package and then
# the imageutils module, which has the function we need
import rsgislib
from rsgislib import imageutils

# Here we just define a string(character) variable with input and output names
# We use relative paths to the main repository folder
inputImage = './data/images/landsat'
inputVector = './data/vectors/'
outputImage = './data/landsat/subset/'

# Here we tell rsgislib that we want a Geotiff file with 8-bit (0-255) data as output
# This are the same file and data type as the opriginal inputs.
# It is a good practice to always specify your output file type and data type
# explicitly, so you always know what kinds of file you are producing.
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8UINT

# Here we run the actual function
imageutils.subset(inputImage, inputVector, outputImage, gdalformat, datatype)
```

In this case, the inputs and outputs never become available in the Python
session. With the exception of `datatype`, all other variables created before
running the funcion were simple text variables.

The advantage of this system is
that functions tend to be faster and more efficient, as they do their own
management of how/when the data is loaded into memory. But that means you are
limited to using the existing functions in the package. A more flexible
alternative is to read your image as a Python/R object, so that you can apply
any function from any package to the data. In Python, the packages that give you
this ability are `raterio` and `rios`.
[Rasterio](https://mapbox.github.io/rasterio/index.html) is a Python package
developed by the [Mapbox](https://www.mapbox.com/) team, meant to be a more
user-friendly interface to the [Geospatial Data Abstraction Library
(GDAL)](http://www.gdal.org/). GDAL is an amazing open library that can tell
other programs how to read and write raster and vector geospatial data. Most
open-source remote sensing and GIS software and packages rely heavily on it (for
example, [QGIS](www.qgis.org), and the RSGISLib package shown above). Although
you can use GDAL direclty from Python, Rasterio makes it more user-friendly.

In
Rasterio, as in many programming tasks, opening a file and reading its contents
are two separate things. The "open" action means only establishing a connection
(pointer) to the file. Once the file is "open", then you can do things to it,
such as get file properties, modify its contents, or, in our case, read the
contents into Python. The main Rasterio funtions for that are `rasterio.open()`
and `rasterio.read()`. Lets see an example:

```python
# As always, we first neet to import the necessary packages
import rasterio

# Then we can open a connection to a file
dataset = rasterio.open("./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B4.TIF")

# Once the connection is made, we can read it.
TM_4 = dataset.read()

# Who is TM_4? A python array!
type(TM_4)
TM_4.shape

# That means we can apply any Pythoin funtion (that accepts an array) to it now.
# What is the average pixel value?
import numpy
numpy.mean(TM_4)
```
