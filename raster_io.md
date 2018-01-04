# Reading remote sensing images into Python and R

There are two main "philosophies" of working with remote sensing images using scripts, that We will call here LOADED and UNLOADED. The UNLOADED way is to simply pass on an image file name that exists on the disk. The function will then do what it is supposed to do with the file, and save the output somewhere else in the disk. This is the `RSGISlib` way. For example, to stack all the bands from our sample Landsat image into a single file, we would use:

```python
import rsgislib
from rsgislib import imageutils

# Listing all band file names that will go into the stack
# Remember to change the path to match your own file organization
imageList = ['./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B1.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B1.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B2.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B3.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B4.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B5.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B6.TIF',
'./images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B7.TIF']

# Names of the bands that will be saved with the file,
# and can be used to specify bands in future processing
bandNamesList = ['TM1','TM2','TM3','TM4','TM5','TM6','TM7']

# Name of the image stack that will be created,
# including the path where it will be saved
outputImage = './images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B1-7.TIF'

# File format and type. Since the original bands are 8-bit unsigned integers
# (0-255), we keep the same format for the output
gdalformat = 'GTiff'
gdaltype = rsgislib.TYPE_8UINT

# The actual stacking function. The extra parameters are
imageutils.stackImageBands(imageList, bandNamesList, outputImage, None, 0, gdalformat, gdaltype)
```




[Rasterio](https://mapbox.github.io/rasterio/index.html) is a Python package developed by the [Mapbox](https://www.mapbox.com/) team, meant to be a more user-friendly interface to the [Geospatial Data Abstraction Library (GDAL)](http://www.gdal.org/). GDAL is an amazing open library that can tell other programs how to read and write raster and vector geospatial data. Most open-source remote sensing and GIS software and packages rely heavily on it (for example, [QGIS](www.qgis.org)).

This guide assumes you have and Anaconda environment set up with Rasterio, and that you have cloned our repository including set of sample Landsat imagery to work with. See the [setup](setup.md) section for details.

The main input fucntion for Rasterio is
