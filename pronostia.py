import urllib.request
import os.path

def download_database():

  url="https://ti.arc.nasa.gov/c/18/"
  urllib.request.urlretrieve(url, "pronostia.zip")
