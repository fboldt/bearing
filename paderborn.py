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
        
    files_path = files_paderborn(dirname)

    print(files_path)
    self.files = files_path

  def segmentate(self):
    """
    Segmentate files by the three main conditions, 
    i.e. Normal, Inner Race and Outer Race.
    It saves the segmented files in three directories,
    i.e. normal, inner and outer.
    NOTE: This is the first idea and it will problably
    be changed in a near future.
    """
    
    dirdest = self.dirdest
    if not os.path.isdir(dirdest):
      os.mkdir(dirdest)
    conditions = {"N":"normal", 
                  "I": "inner", 
                  "O": "outer"}
    for key, condition in conditions.items():
      if not os.path.isdir(os.path.join(dirdest, condition)):
        os.mkdir(os.path.join(dirdest, condition))
    files_names = self.files
    acquisitions = get_tensors_from_files(files_names, self.rawfilesdir)
    sample_size=8192
    data = np.empty((0,sample_size,1))
    n = len(acquisitions)
    for i,key in enumerate(acquisitions):
      acquisition_size = len(acquisitions[key])
      n_samples = acquisition_size//sample_size
      print('{}/{} --- {}: {}'.format(i+1, n, key, n_samples))
      data = acquisitions[key][:(n_samples*sample_size)].reshape((n_samples,sample_size,1))
      for j in range(n_samples):
        file_name = os.path.join(dirdest, conditions[key[5]], key+str(j)+'.csv')
        if not os.path.exists(file_name):
          np.savetxt(file_name, data[j], delimiter=',')
          
def files_paderborn(dirfiles):
  """
  Associate each file name to a bearing condition in a Python dictionary. 
  The dictionary keys identify the conditions.
  
  In total, experiments with 32 different bearings were performed:
  12 bearings with artificial damages and 14 bearings with damages
  from accelerated lifetime tests. Moreover, experiments with 6 healthy
  bearings and a different time of operation were performed as
  reference states.
 
  The rotational speed of the drive system, the radial force onto the test
  bearing and the load torque in the drive train are the main operation
  parameters. To ensure comparability of the experiments, fixed levels were
  defined for each parameter. All three parameters were kept constant for
  the time of each measurement. At the basic setup (Set no. 0) of the 
  operation parameters, the test rig runs at n = 1,500 rpm with a load 
  torque of M = 0.7 Nm and a radial force on the bearing of F = 1,000 N. Three
  additional settings are used by reducing the parameters one
  by one to n = 900 rpm, M = 0.1 Nm and F = 400 N (set No. 1-3), respectively.
  
  For each of the settings, 20 measurements of 4 seconds each were recorded
  for each bearing. There are a total of 2.560 files.

  All files start with the bearing code, followed by the conditions, by an
  algarism representing the setting and end with an algarism representing 
  the sample sequential. All features are separated by an underscore character.
  """
  files_path = {}
  
  normal_folder = ["K001", "K002", "K003", "K004", "K005", "K006"]
  OR_folder = ["KA01", "KA03", "KA04", "KA05", "KA06", "KA07", "KA08", 
              "KA09", "KA15", "KA16", "KA22", "KA30"]
  IR_folder = ["KI01", "KI03", "KI05", "KI07", "KI08", "KI16", "KI17", 
              "KI18", "KI21"]
  MIX_folder = ["KB23", "KB24", "KB27", "KI14"] # VERIFICAR

  settings_files = ["N15_M07_F10_", "N09_M07_F10_", "N15_M01_F10_", "N15_M07_F04_"]

  n = 20 #Number of samples for each setting

  # Normal
  for folder in normal_folder:
    for idx, setting in enumerate(settings_files):
      for i in range(1, n+1):
        key = folder + "_Normal_" + str(idx) + "_" + str(i)
        files_path[key] = os.path.join(dirfiles, folder, setting + folder +
                                       "_" + str(i) + ".mat")

  # OR
  for folder in OR_folder:
    for idx, setting in enumerate(settings_files):
      for i in range(1, n+1):
        key = folder + "_OR_" + str(idx) + "_" + str(i)
        files_path[key] = os.path.join(dirfiles, folder, setting + folder +
                                       "_" + str(i) + ".mat")

  # IR
  for folder in IR_folder:
    for idx, setting in enumerate(settings_files):
      for i in range(1, n+1):
        key = folder + "_IR_" + str(idx) + "_" + str(i)
        files_path[key] = os.path.join(dirfiles, folder, setting + folder +
                                       "_" + str(i) + ".mat")

  return files_path


def get_tensors_from_files(files_names, rawfilesdir=""):
  """
  Extracts the acquisitions of each file in the dictionary files_names.
  The user must be careful because this function converts all files
  in the files_names in numpy arrays.
  As large the number of entries in files_names 
  as large will be the space of memory necessary.

  Atributes
  ---------
  files_names : dict
    the keys represent the conditions and the values are the file names
  rawfilesdir : str
    directory where the files are
  
  Returns
  -------
  acquisitions : dict
  The keys represent the bearing code, followed by the conditions, by an
  algarism representing the setting and end with an algarism representing 
  the sample sequential. All features are separated by an underscore character.
  """

  acquisitions = {}
  for key in files_names:
    if key != 'KA08_OR_2_2': # Dsiconsider this file (apparently corrupted)
      matlab_file = scipy.io.loadmat(files_names[key])
      if len(files_names[key])>40:
        vibration_data=matlab_file[files_names[key][18:37]]['Y'][0][0][0][6][2]
      else:
        vibration_data=matlab_file[files_names[key][18:36]]['Y'][0][0][0][6][2]

    print(key)
    acquisitions[key] = vibration_data[0]

  return acquisitions
