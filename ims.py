import urllib.request
import os.path

def download_database():
  url="https://ti.arc.nasa.gov/c/3/"
  urllib.request.urlretrieve(url, "IMS.7z")
