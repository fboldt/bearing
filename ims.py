"""
Class definition of IMS datasest.
"""

# Author: Lucio Venturim <lucioventurim@gmail.com> 
# Francisco Boldt <fboldt@gmail.com>

import urllib.request
import os
import database
import scipy.io
import numpy as np
from os import listdir
from os.path import isfile, join

# Unpack Tools
!pip install pyunpack
!pip install patool
from pyunpack import Archive


class IMS(database.Database):
  """
  IMS class wrapper for experiment framework.
  """
  def __init__(self):
    #self.files = files_IMS()
    self.rawfilesdir = "database_raw"
    self.dirdest = "database"
    self.url="https://ti.arc.nasa.gov/c/3/"

  def download(self):
    """
    Download Matlab files from NASA website.
    """
    url = self.url
    urllib.request.urlretrieve(url, "IMS.7z")
    
    dirname = self.rawfilesdir
    if not os.path.isdir(dirname):
      os.mkdir(dirname)
    
    Archive('IMS.7z').extractall(dirname)
    Archive(os.path.join(dirname, '1st_test.rar')).extractall(dirname)
    Archive(os.path.join(dirname, '3rd_test.rar')).extractall(dirname)
    files_names = files_IMS(dirname)

    print(files_names)
    
  def segmentate(self):
      pass
   
  
def files_IMS(dirfiles):
  """
  Associate each Matlab file name to a bearing condition in a Python dictionary. 
  The dictionary keys identify the conditions.
  
  Data taken from channel 1 of test 1 from 12:06:24 on 23/10/2003 
  to 13:05:58 on 09/11/2003 were considered normal. For inner race fault and 
  rolling element fault, data were taken from 08:22:30 on 18/11/2003 
  to 23:57:32 on 24/11/2003 from channel 5 and channel 7 respectively. 
  Outer race fault data were taken from channel 3 of test 4 from 14:51:57 
  on 12/4/2004 to 02:42:55 on 18/4/2004. 
  
  There are a total of 750 files in each category.
  All normal conditions end with an underscore character followed by an algarism 
  representing the sequence of the acquisitions. 
  The remaining conditions follow the pattern:
  
  First two characters represent the failure location in the bearing, 
  i.e. ball (BA), Inner Race (IR) and Outer Race (OR).
  """
  files_names = {}
  
  first_test_path = os.path.join(dirfiles,"1st_test")
  fourth_test_path = os.path.join(dirfiles,"4th_test","txt")

  first_test_files = [f for f in listdir(first_test_path) if isfile(join(first_test_path, f))]
  first_test_files.sort()
  print(first_test_files)
  
  fourth_test_files = [f for f in listdir(fourth_test_path) if isfile(join(fourth_test_path, f))]
  fourth_test_files.sort()
  print(fourth_test_files)
  
  n = 750

  # Normal
  for i in range(1, n+1):
    key = "Normal_" + str(i).zfill(4)
    files_names[key] = first_test_files[i-1]

  # Inner
  for i in range(1370, n+1370):
    key = "IR_" + str(i).zfill(4)
    files_names[key] = first_test_files[i-1]

  # Ball
  for i in range(1370, n+1370):
    key = "BA_" + str(i).zfill(4)
    files_names[key] = first_test_files[i-1]

  # Outer
  for i in range(5575, n+5575):
    key = "OR_" + str(i).zfill(4)
    files_names[key] = fourth_test_files[i-1]

  return files_names
