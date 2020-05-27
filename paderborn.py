"""
Class definition of Paderborn Bearing datasest.
"""

# Author: Lucio Venturim <lucioventurim@gmail.com> 
# Francisco Boldt <fboldt@gmail.com>

import urllib.request
import os
import database  # used in GitHub
import scipy.io
import numpy as np
from os import listdir
from os.path import isfile, join

# Unpack Tools
!pip install pyunpack
!pip install patool
from pyunpack import Archive


class Paderborn(database.Database): #database.Database # used in GitHub
  """
  Paderborn class wrapper for experiment framework.

  ...
  Attributes
  ----------
  rawfilesdir : str
    directory name where the files will be downloaded
  dirdest : str
    directory name of the segmented files
  url : str
    website from the raw files are downloaded
  files : dict
    the keys represent the conditions and the values are the files names
  
  Methods
  -------
  download()
    Download raw compressed files from Paderborn website
  segmentate()
    Semgmentate the raw files in various .csv files
  """
  def __init__(self):
    self.rawfilesdir = "database_raw"
    self.dirdest = "database"
    self.url="http://groups.uni-paderborn.de/kat/BearingDataCenter/"

  def download(self):
    """
    Download and extract compressed files from Paderborn website.

    It may be used to keep the matlab files as a cache memory.
    Once downloaded the compressed file, it does not need to be downoaded again.
    """
    
    # RAR Files names
    rar_files_name = ["K001.rar","K002.rar","K003.rar","K004.rar","K005.rar","K006.rar",
                  "KA01.rar", "KA03.rar", "KA04.rar", "KA05.rar", "KA06.rar", "KA07.rar", 
                  "KA08.rar", "KA09.rar", "KA15.rar", "KA16.rar", "KA22.rar", "KA30.rar", 
                  "KB23.rar", "KB24.rar", "KB27.rar", 
                  "KI01.rar", "KI03.rar", "KI04.rar", "KI05.rar", "KI07.rar", "KI08.rar", 
                  "KI14.rar", "KI16.rar", "KI17.rar", "KI18.rar", "KI21.rar"]
       
    url = self.url
    
    print("Donwloading RAR files:")
    for i in rar_files_name:
      file_name = i
      if not os.path.exists(file_name):
        urllib.request.urlretrieve(url+file_name, file_name)
      print(file_name)
    
    
    dirname = self.rawfilesdir
    if not os.path.isdir(dirname):
      os.mkdir(dirname)
    
    print("Extracting files:")
    for i in rar_files_name:
      file_name = i
      Archive(i).extractall(dirname)  
      print(file_name)
        
    #files_names = files_paderborn(dirname)

    #print(files_names)
    #self.files = files_names

  def segmentate(self):
    pass
