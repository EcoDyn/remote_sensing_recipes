# Reading remote sensing images into Python and R

> This guide assumes you have
> a Python Anaconda environment set up with `GDAL`,`rasterio`, `rsgislib` and `rios`, and that
>
> you have ran the necessary setup scripts to download the example data. See the
> [setup](setup.md) section for details.

There are two main "philosophies" of working with remote sensing images using `python` or `R`scripts, which we will call here "*loaded* " and "*on disk*".  The *on disk*  way is to simply pass on
image filenames to functions as that exist on disk. The function will then do what
it is supposed to do with the file, and write the results to disk, but the
file never becomes a variable/object that is "*loaded* " into the `python` or `R`
environment, so it can be accessed and processed by functions within your working session. 

#### Reading remote sensing images into `pyhton`

Working "*on disk*" is the `RSGISlib` and `GDAL`way. Let say we are writing a `python` script to subset an image using a polygon shapefile:

```python
# First step is to import the rsgislib package and then
# the imageutils module, which has the function we need
import rsgislib
from rsgislib import imageutils

# Here we just define a string(character) variable with input and output file names
# We show here relative paths to the main repository folder, but absolute paths are also possible
inputImage = './data/images/landsat'
inputVector = './data/vectors/'
outputImage = './data/landsat/subset/'

# Here we define the function parameters that will tell to the rsgislib function
# that we want a Geotiff file with 8-bit (0-255) data as output.
# These are the same file and datatype as the opriginal inputs. Some functions will
# use the same format and datatype as the inputs if none are given default, others
# will have preset defaults.
# But it is a good practice to always be explicit about your output file type and 
# datatype, so you are always sure of what kinds of file you are producing, and that you 
# are not wasting unnecessary bytes and disk space.
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8UINT # See https://www.rsgislib.org/rsgislib.html

# Here we run the actual function
imageutils.subset(inputImage, inputVector, outputImage, gdalformat, datatype)
```

In this case, the inputs and outputs never become available as variables in the `python` session. With the exception of `datatype`, which calls for a specific method of `rsgislib`, all other variables created before calling the `imageutils.subset` function were simple text variables.

The advantage of this system is that functions tend to be faster and more efficient, as they do their own
management of how/when the data is loaded into memory, in a (hopefully) optimal way. But that means you are limited to using the existing functions in the package. 

A more flexible alternative is to read your image as a `python` or `R` object, so that you can use any available function from any existing package to process the data, or even write your own functions. In Python, the packages that give you this ability are `rasterio` and `rios`. [Rasterio](https://mapbox.github.io/rasterio/index.html) is a Python package developed by the [Mapbox](https://www.mapbox.com/) team, meant to be a more user-friendly interface to the [Geospatial Data Abstraction Library (GDAL)](http://www.gdal.org/). `GDAL` is an amazing open library that can tell other programs how to read and write raster and vector geospatial data, and also has very efficient functions for mosaicking, stackinf, subsestting and converting data. Most open-source remote sensing and GIS applications and packages rely heavily on it (for example, [QGIS](www.qgis.org), and the [RSGISLib](www.rsgislib,org) package shown above). Although you can use `GDAL direclty` from the command line or as a `python` module, `rasterio` makes it more user-friendly and straightforward. 

In `rasterio`, as in many programming tasks, opening a file and reading its contents are two separate things. The "open" action means only establishing a connection (pointer) to the file. Once the file is "open", then you can do things to it, such as get file properties, modify its contents, or, in our case, read the contents into `python`. The main `rasterio` functions for that are `rasterio.open()` and  `rasterio.read()`. Lets see an example:

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

# That means we can apply any Python function (that accepts an array) to it now.
# What is the average pixel value?
import numpy
numpy.mean(TM_4)
```



#### Reading remote sensing images into `R`

In `R` , the amazing `raster` package is almost all you need to work with remote sensing images and GIS data. Other packages complement and build upon it , such as `rasterVis`, `satellite`, `spatial.tools` and dozens of others.  As mentioned, `raster` makes use of `GDAL` for input and output, meaning it supports a huge array of file formats. 

Another very important aspect of `raster` is that it is able to process raster data out-of-memory, removing one of the main limitations of processing remote sensing data in `R`. It will not be very fast, but it gets the job done. In this sense, it is a "hybrid" between working *loaded* and *on disk*. It will be visible to `R`functions like any other `R `object, and the package will provide internal methods to apply these functions to the data as if it was loaded on memory. Here is  how we use it:

```R
# Load the raster package
library(raster)

# Create an R object pointing to the raster file. 'dataset' will not contain the raster data itself, but will let R know how to handle the data on disk. Unlike on python/rasterio, don't need to read it into memory.
TM_4 <-raster("./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B4.TIF")

# Who is TM_4? A raster object!
TM_4
dim(TM_4)

# That means we can apply many R functions to it now.
# What is the average pixel value?
mean(TM_4)
```

