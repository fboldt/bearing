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
from numpy import genfromtxt

# Unpack Tools
import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyunpack'])
from pyunpack import Archive

# Tools used in Jupyter Notebooks
#!pip install pyunpack
#!pip install patool
#!from pyunpack import Archive


class IMS(database.Database):
  """
  IMS class wrapper for experiment framework.

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
    Download raw compressed files from NASA website
  segmentate()
    Semgmentate the raw files in various .csv files
  """
  def __init__(self):
    #self.files = files_IMS()
    self.rawfilesdir = "database_raw"
    self.dirdest = "database"
    self.url="https://ti.arc.nasa.gov/c/3/"

  def download(self):
    """
    Download and extract compressed files from NASA website.

    It may be used to keep the matlab files as a cache memory.
    Once downloaded the compressed file, it does not need to be downoaded again.
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
    self.files = files_names
    
  def segmentate(self):
    """
    Segmentate files by the four main conditions, 
    i.e. Normal, Ball, Inner Race and Outer Race.
    It saves the segmented files in four directories,
    i.e. normal, ball, inner and outer.
    NOTE: This is the first idea and it will problably
    be changed in a near future.
    """
    
    dirdest = self.dirdest
    if not os.path.isdir(dirdest):
      os.mkdir(dirdest)
    conditions = {"N":"normal", 
                  "B": "ball", 
                  "I": "inner", 
                  "O": "outer"}
    for key, condition in conditions.items():
      if not os.path.isdir(os.path.join(dirdest, condition)):
        os.mkdir(os.path.join(dirdest, condition))
    files_names = self.files
    acquisitions = get_tensors_from_files(files_names, self.rawfilesdir)
    sample_size=1024
    data = np.empty((0,sample_size,1))
    n = len(acquisitions)
    for i,key in enumerate(acquisitions):
      acquisition_size = len(acquisitions[key])
      n_samples = acquisition_size//sample_size
      print('{}/{} --- {}: {}'.format(i+1, n, key, n_samples))
      data = acquisitions[key][:(n_samples*sample_size)].reshape((n_samples,sample_size,1))
      for j in range(n_samples):
        file_name = os.path.join(dirdest, conditions[key[0]], key+str(j)+'.csv')
        if not os.path.exists(file_name):
          np.savetxt(file_name, data[j], delimiter=',')
   
  
def files_IMS(dirfiles):
  """
  Associate each file name to a bearing condition in a Python dictionary. 
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
  i.e. ball (BA), Inner Race (IR) and Outer Race (OR). All fault conditions end
  with an underscore character followed by an algarism representing the 
  sequence of the acquisitions.
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

def get_tensors_from_files(files_names, rawfilesdir=""):
  """
  Extracts the acquisitions of each file in the dictionary files_names.
  The user must be careful because this function converts all files
  in the files_names in numpy arrays.
  As large the number of entries in files_names 
  as large will be the space of memory necessary.
  
  IMS dataset files have 7 channels on the test 1 set and 4 channels on the 
  test 4 set. Data taken from channel 1 of test 1 were considered normal.
  For inner race fault and rolling element fault, data were taken from 
  channel 5 and channel 7 respectively.
  Outer race fault data were taken from channel 3 of test 4.

  Atributes
  ---------
  files_names : dict
    the keys represent the conditions and the values are the file names
  rawfilesdir : str
    directory where the files are
  
  Returns
  -------
  acquisitions : dict
    the keys represent the condition and the acquisition sequential and
    the values are numpy arrays with the acquired signal in the time domain.
  """

  acquisitions = {}
  
  for key in files_names:
    if "OR" in key:
      file_name = os.path.join(rawfilesdir, "4th_test", "txt", files_names[key])
    else:
      file_name = os.path.join(rawfilesdir, "1st_test", files_names[key])
    
    file_data = genfromtxt(file_name, unpack=True)
    
    if "Normal" in key:
      acquisitions[key] = file_data[0]
    elif "IR" in key:
      acquisitions[key] = file_data[4]
    elif "OR" in key:
      acquisitions[key] = file_data[2]
    else:
      acquisitions[key] = file_data[6]

  return acquisitions

def main():
  database = IMS()
  database.download()
  database.segmentate()

if __name__ == "__main__":
  main()
