"""
Class definition of MFPT Bearing datasest.
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
import subprocess
import sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyunpack'])
from pyunpack import Archive

# Tools used in Jupyter Notebooks
#!pip install pyunpack
#!pip install patool
#!from pyunpack import Archive

class MFPT(database.Database): #database.Database # used in GitHub
  """
  MFPT class wrapper for experiment framework.

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
    Download raw compressed files from MFPT website
  segmentate()
    Semgmentate the raw files in various .csv files
  """
  def __init__(self, debug=0):
    self.debug=debug
    self.rawfilesdir = "mfpt_raw"
    self.dirdest = "mfpt_seg"
    self.url="https://mfpt.org/wp-content/uploads/2020/02/MFPT-Fault-Data-Sets-20200227T131140Z-001.zip"
    self.sample_rate = 97656
    self.conditions = {"N":"normal", 
              "I": "inner", 
              "O": "outer"}

  def download(self):
    """
    Download and extract compressed files from MFPT website.

    It may be used to keep the matlab files as a cache memory.
    Once downloaded the compressed file, it does not need to be downoaded again.
    """

    url = self.url
    
    dirname = self.rawfilesdir
    if not os.path.isdir(dirname):
      os.mkdir(dirname)
    
    zip_name = "MFPT-Fault-Data-Sets-20200227T131140Z-001.zip"

    print("Donwloading ZIP file")
    
    urllib.request.urlretrieve(url, os.path.join(dirname, zip_name))

    print("Extracting files")
    file_name = os.path.join(dirname, zip_name)
    Archive(file_name).extractall(dirname)

    self.files = files_mfpt(dirname)
    print(self.files)

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

    for key, condition in self.conditions.items():
      if not os.path.isdir(os.path.join(dirdest, condition)):
        os.mkdir(os.path.join(dirdest, condition))
    files_names = self.files
    self.acquisitions = get_tensors_from_files(files_names, self.rawfilesdir)
    self.descr = dict.fromkeys(self.conditions.keys(),0)
    self.sample_size=8192
    data = np.empty((0,self.sample_size,1))
    n = len(self.acquisitions)
    for i,key in enumerate(self.acquisitions):
      acquisition_size = len(self.acquisitions[key])
      n_samples = acquisition_size//self.sample_size
      self.descr[key[0]] += n_samples
      print('{}/{} --- {}: {}'.format(i+1, n, key, n_samples))
      data = self.acquisitions[key][:(n_samples*self.sample_size)].reshape((n_samples,self.sample_size,1))
      for j in range(n_samples):
        file_name = os.path.join(dirdest, self.conditions[key[0]], key+str(j)+'.csv')
        if not os.path.exists(file_name):
          np.savetxt(file_name, data[j], delimiter=',')

  def description(self):
    """
    Provides a brief description of the dataset.
    """
    
    description_dict = {}
    description_dict['n_acquisitions'] = len(self.acquisitions)
    description_dict['sample_rate'] = self.sample_rate
    description_dict['sample_size'] = self.sample_size
    
    classes = self.descr
      
    samples = 0
       
    for key in classes:
      description_dict['class_'+self.conditions[key]] = classes[key]
      samples = samples + classes[key]

    description_dict['class_total_samples'] = samples

    return description_dict


def files_mfpt(dirfiles):
  """
  Associate each file name to a bearing condition in a Python dictionary. 
  The dictionary keys identify the conditions.
  
  The MFPT dataset is divided into 3 kinds of states: normal state, inner race
  fault state, and outer race fault state (N, IR, and OR), where three baseline
  data were gathered at a sampling frequency of 97656 Hz and under 270 lbs of
  load; seven outer race fault data were gathered at a sampling frequency of
  48828 Hz and, respectively, under 25, 50, 100, 150, 200, 250, and 300 lbs 
  of load, and seven inner race fault data were gathered at a sampling 
  frequency of 48828 Hz and, respectively, under 0, 50, 100, 150, 200, 250, 
  and 300 lbs of load.

  """
  files_path = {}
  
  # Normal
  files_path["Normal_0"] = os.path.join(dirfiles, "MFPT Fault Data Sets/1 - Three Baseline Conditions/baseline_1")
  files_path["Normal_1"] = os.path.join(dirfiles, "MFPT Fault Data Sets/1 - Three Baseline Conditions/baseline_2")
  files_path["Normal_2"] = os.path.join(dirfiles, "MFPT Fault Data Sets/1 - Three Baseline Conditions/baseline_3")
  # OR
  files_path["OR_0"] = os.path.join(dirfiles, "MFPT Fault Data Sets/2 - Three Outer Race Fault Conditions/OuterRaceFault_1")
  files_path["OR_1"] = os.path.join(dirfiles, "MFPT Fault Data Sets/2 - Three Outer Race Fault Conditions/OuterRaceFault_2")
  files_path["OR_2"] = os.path.join(dirfiles, "MFPT Fault Data Sets/2 - Three Outer Race Fault Conditions/OuterRaceFault_3")
  files_path["OR_3"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_1")
  files_path["OR_4"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_2")
  files_path["OR_5"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_3")
  files_path["OR_6"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_4")
  files_path["OR_7"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_5")
  files_path["OR_8"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_6")
  files_path["OR_9"] = os.path.join(dirfiles, "MFPT Fault Data Sets/3 - Seven More Outer Race Fault Conditions/OuterRaceFault_vload_7")
  # IR
  files_path["IR_0"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_1")
  files_path["IR_1"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_2")
  files_path["IR_2"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_3")
  files_path["IR_3"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_4")
  files_path["IR_4"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_5")
  files_path["IR_5"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_6")
  files_path["IR_6"] = os.path.join(dirfiles, "MFPT Fault Data Sets/4 - Seven Inner Race Fault Conditions/InnerRaceFault_vload_7")

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
    matlab_file = scipy.io.loadmat(files_names[key])
    #print(matlab_file)
    if len(key) == 8:
      vibration_data_raw = matlab_file['bearing'][0][0][1]
    else:
      vibration_data_raw = matlab_file['bearing'][0][0][2]
    
    vibration_data = np.array([ elem for singleList in vibration_data_raw for elem in singleList])

    acquisitions[key] = vibration_data
  #print(acquisitions)
  return acquisitions
  
def main():
  database = MFPT()
  database.download()
  database.segmentate()
  database.description()

if __name__ == "__main__":
  main()
