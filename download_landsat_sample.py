# This script will download aand unzip a sample Landsat image used to demonstrate several
# of the recipes
import wget

url = 'https://drive.google.com/open?id=1StYTvGlSPrs2qLjEo0Ivq-a234qXolxr'
wget.download(url, './data/images/landsat/landsat_example.zip')
