# Stacking, resampling and subsetting images in Python and R

This section comprises a collection of remote sensing tasks usually referredo to as "pre-processing", which include several things such as stacking sepearte band files into a single file, subsetting an image, changing resolution, assigning prjections, and so on.

## Stacking image bands

Different image providers will give you imagery in different file formats (GeoTIFF, HDF, etc.), and often using different file structures (e.g. one file per band *vs.* multiple bands in a single file), with advantages and disadvantages to each combination. Often times, image processing algorithms will require that all bands are contained within a single file or object. We show here different way to accomplish this in Python and R.

In Python, we can create a new, stacked file using the `rsgislib` function `stackImageBands`, from the `imageutils` module.

```python
# Importing the necessary packages
import os
import rsgislib
from rsgislib import imageutils

# First we create a new output directory for our stacked image to be stored
os.mkdir('./data/images/landsat/stacked/')

# Then we need to define a list of images to be stacked
imageList = ["./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B1.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B2.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B3.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B4.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B5.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B6.TIF", "./data/images/landsat/LT05_L1TP_231062_20090910_20161020_01_T1_B7.TIF"]

# We can name the bands, so we can use the names to access them later
bandNamesList = ['B1','B2','B3','B4','B5','B6','B7']

# We then specify a name and path for the stacked image that will be created
# We always recommend having long, informative names that give you a history
# So we keep the original naming and only modify the  ending
outputImage = './data/images/landsat/stacked/LT05_L1TP_231062_20090910_20161020_01_T1_B1-7_stack.TIF'

# We must tell RSGISlib the file and data format we want
gdalformat = 'GTiff'
gdaltype = rsgislib.TYPE_8UINT

# And then we can apply the function
imageutils.stackImageBands(imageList, bandNamesList, outputImage, None, 0, gdalformat, gdaltype)
```
And *voilá*, we have created a new file with all seven Landsat 5 TM bands. We can now do further processing of this file using `rsgislib`, or load it into our working environment using `rasterio.

```python
import rasterio

# We can reuse the output file name stored before if we are still
#  working within the same session
dataset = rasterio.open(outputImage)
TM_img = dataset.read()

# Who is TM_img?
type(TM_img)
TM_img.shape

# We can read in only some of the bands, if we dont need them all
TM_BGR = dataset.read([1,2,3])
TM_BGR.shape
```
