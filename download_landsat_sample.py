# This script will download aand unzip a sample Landsat image used to demonstrate several
# of the recipes

from urllib.request import urlopen
from zipfile import ZipFile
zipurl = 'https://drive.google.com/open?id=1StYTvGlSPrs2qLjEo0Ivq-a234qXolxr'
# Download the file from the URL
zipresp = urlopen(zipurl)
# Create a new file on the hard drive
tempzip = open("/tmp/tempfile.zip", "wb")
# Write the contents of the downloaded file into the new file
tempzip.write(zipresp.read())
# Close the newly-created file
tempzip.close()
# Re-open the newly-created file with ZipFile()
zf = ZipFile("/tmp/tempfile.zip")
# Extract its contents into /tmp/mystuff
# note that extractall will automatically create the path
zf.extractall(path = "./data/images/landsat/')
# close the ZipFile instance
zf.close()
