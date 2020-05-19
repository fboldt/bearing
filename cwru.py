"""
Class definition of CWRU datasest.
"""

# Author: Lucio Venturim <lucioventurim@gmail.com> 
# Francisco Boldt <fboldt@gmail.com>

import urllib.request
import os
import database
import scipy.io
import numpy as np

class CWRU(database.Database):
  """
  CWRU class wrapper for experiment framework.
  """
  def __init__(self):
    self.files = files_12khz()
    self.rawfilesdir = "database_raw"
    self.dirdest = "database"
    self.url="http://csegroups.case.edu/sites/default/files/bearingdatacenter/files/Datafiles/"

  def download(self):
    """
    Download Matlab files from CWRU website.
    """
    matlab_files_name = self.files
    url = self.url
    n = len(matlab_files_name)
    dirname = self.rawfilesdir
    if not os.path.isdir(dirname):
      os.mkdir(dirname)
    for i,key in enumerate(matlab_files_name):
      file_name = matlab_files_name[key]
      if not os.path.exists(os.path.join(dirname, file_name)):
        urllib.request.urlretrieve(url+file_name, os.path.join(dirname, file_name))
      print("{}/{}\t{}\t{}".format(i+1, n, key, file_name))
  
  def segmentate(self):
    """
    Segmentate Matlab files by main condition, i.e. Normal, Ball, InnerRace and OuterRace.
    """
    dirdest = self.dirdest
    if not os.path.isdir(dirdest):
      os.mkdir(dirdest)
    conditions = {"r":"normal", 
                  "B": "ball", 
                  "I": "inner", 
                  "O": "outer"}
    for key, condition in conditions.items():
      if not os.path.isdir(os.path.join(dirdest, condition)):
        os.mkdir(os.path.join(dirdest, condition))
    matlab_files_name = self.files
    acquisitions = get_tensors_from_matlab(matlab_files_name, self.rawfilesdir)
    sample_size=512
    data = np.empty((0,sample_size,1))
    n = len(acquisitions)
    for i,key in enumerate(acquisitions):
      acquisition_size = len(acquisitions[key])
      n_samples = acquisition_size//sample_size
      print('{}/{} --- {}: {}'.format(i+1, n, key, n_samples))
      data = acquisitions[key][:(n_samples*sample_size)].reshape((n_samples,sample_size,1))
      for j in range(n_samples):
        file_name = os.path.join(dirdest, conditions[key[2]], key+str(j)+'.csv')
        if not os.path.exists(file_name):
          np.savetxt(file_name, data[j], delimiter=',')

def files_12khz():
  """
  Associate each Matlab file name to a bearing condition in a Python dictionary. 
  The dictionary keys identify the conditions.
  
  There are only four normal conditions, with loads of 0, 1, 2 and 3 hp. 
  All conditions end with an underscore character followed by an algarism 
  representing the load applied during the acquisitions. 
  The remaining conditions follow the pattern:
  
  First two characters represent the bearing location, 
  .e. drive end (DE) and fan end (FE). 
  The following two characters represent the failure location in the bearing, 
  i.e. ball (BA), Inner Race (IR) and Outer Race (OR). 
  The next three algarisms indicate the severity of the failure, 
  where 007 stands for 0.007 inches and 0021 for 0.021 inches. 
  For Outer Race failures, the character @ is followed by a number 
  that indicates different load zones.
  """
  matlab_files_name = {}
  # Normal
  matlab_files_name["Normal_0"] = "97.mat"
  matlab_files_name["Normal_1"] = "98.mat"
  matlab_files_name["Normal_2"] = "99.mat"
  matlab_files_name["Normal_3"] = "100.mat"
  # DE Inner Race 0.007 inches
  matlab_files_name["DEIR.007_0"] = "105.mat"
  matlab_files_name["DEIR.007_1"] = "106.mat"
  matlab_files_name["DEIR.007_2"] = "107.mat"
  matlab_files_name["DEIR.007_3"] = "108.mat"
  # DE Ball 0.007 inches
  matlab_files_name["DEB.007_0"] = "118.mat"
  matlab_files_name["DEB.007_1"] = "119.mat"
  matlab_files_name["DEB.007_2"] = "120.mat"
  matlab_files_name["DEB.007_3"] = "121.mat"
  # DE Outer race 0.007 inches centered @6:00
  matlab_files_name["DEOR.007@6_0"] = "130.mat"
  matlab_files_name["DEOR.007@6_1"] = "131.mat"
  matlab_files_name["DEOR.007@6_2"] = "132.mat"
  matlab_files_name["DEOR.007@6_3"] = "133.mat"
  # DE Outer race 0.007 inches centered @3:00
  matlab_files_name["DEOR.007@3_0"] = "144.mat"
  matlab_files_name["DEOR.007@3_1"] = "145.mat"
  matlab_files_name["DEOR.007@3_2"] = "146.mat"
  matlab_files_name["DEOR.007@3_3"] = "147.mat"
  # DE Outer race 0.007 inches centered @12:00
  matlab_files_name["DEOR.007@12_0"] = "156.mat"
  matlab_files_name["DEOR.007@12_1"] = "158.mat"
  matlab_files_name["DEOR.007@12_2"] = "159.mat"
  matlab_files_name["DEOR.007@12_3"] = "160.mat"
  # DE Inner Race 0.014 inches
  matlab_files_name["DEIR.014_0"] = "169.mat"
  matlab_files_name["DEIR.014_1"] = "170.mat"
  matlab_files_name["DEIR.014_2"] = "171.mat"
  matlab_files_name["DEIR.014_3"] = "172.mat"
  # DE Ball 0.014 inches
  matlab_files_name["DEB.014_0"] = "185.mat"
  matlab_files_name["DEB.014_1"] = "186.mat"
  matlab_files_name["DEB.014_2"] = "187.mat"
  matlab_files_name["DEB.014_3"] = "188.mat"
  # DE Outer race 0.014 inches centered @6:00
  matlab_files_name["DEOR.014@6_0"] = "197.mat"
  matlab_files_name["DEOR.014@6_1"] = "198.mat"
  matlab_files_name["DEOR.014@6_2"] = "199.mat"
  matlab_files_name["DEOR.014@6_3"] = "200.mat"
  # DE Ball 0.021 inches
  matlab_files_name["DEB.021_0"] = "222.mat"
  matlab_files_name["DEB.021_1"] = "223.mat"
  matlab_files_name["DEB.021_2"] = "224.mat"
  matlab_files_name["DEB.021_3"] = "225.mat"
  # FE Inner Race 0.021 inches
  matlab_files_name["FEIR.021_0"] = "270.mat"
  matlab_files_name["FEIR.021_1"] = "271.mat"
  matlab_files_name["FEIR.021_2"] = "272.mat"
  matlab_files_name["FEIR.021_3"] = "273.mat"
  # FE Inner Race 0.014 inches
  matlab_files_name["FEIR.014_0"] = "274.mat"
  matlab_files_name["FEIR.014_1"] = "275.mat"
  matlab_files_name["FEIR.014_2"] = "276.mat"
  matlab_files_name["FEIR.014_3"] = "277.mat"
  # FE Ball 0.007 inches
  matlab_files_name["FEB.007_0"] = "282.mat"
  matlab_files_name["FEB.007_1"] = "283.mat"
  matlab_files_name["FEB.007_2"] = "284.mat"
  matlab_files_name["FEB.007_3"] = "285.mat"
  # DE Inner Race 0.021 inches
  matlab_files_name["DEIR.021_0"] = "209.mat"
  matlab_files_name["DEIR.021_1"] = "210.mat"
  matlab_files_name["DEIR.021_2"] = "211.mat"
  matlab_files_name["DEIR.021_3"] = "212.mat"
  # DE Outer race 0.021 inches centered @6:00
  matlab_files_name["DEOR.021@6_0"] = "234.mat"
  matlab_files_name["DEOR.021@6_1"] = "235.mat"
  matlab_files_name["DEOR.021@6_2"] = "236.mat"
  matlab_files_name["DEOR.021@6_3"] = "237.mat"
  # DE Outer race 0.021 inches centered @3:00
  matlab_files_name["DEOR.021@3_0"] = "246.mat"
  matlab_files_name["DEOR.021@3_1"] = "247.mat"
  matlab_files_name["DEOR.021@3_2"] = "248.mat"
  matlab_files_name["DEOR.021@3_3"] = "249.mat"
  # DE Outer race 0.021 inches centered @12:00
  matlab_files_name["DEOR.021@12_0"] = "258.mat"
  matlab_files_name["DEOR.021@12_1"] = "259.mat"
  matlab_files_name["DEOR.021@12_2"] = "260.mat"
  matlab_files_name["DEOR.021@12_3"] = "261.mat"
  # FE Inner Race 0.007 inches
  matlab_files_name["FEIR.007_0"] = "278.mat"
  matlab_files_name["FEIR.007_1"] = "279.mat"
  matlab_files_name["FEIR.007_2"] = "280.mat"
  matlab_files_name["FEIR.007_3"] = "281.mat"
  # FE Ball 0.014 inches
  matlab_files_name["FEB.014_0"] = "286.mat"
  matlab_files_name["FEB.014_1"] = "287.mat"
  matlab_files_name["FEB.014_2"] = "288.mat"
  matlab_files_name["FEB.014_3"] = "289.mat"
  # FE Ball 0.021 inches
  matlab_files_name["FEB.021_0"] = "290.mat"
  matlab_files_name["FEB.021_1"] = "291.mat"
  matlab_files_name["FEB.021_2"] = "292.mat"
  matlab_files_name["FEB.021_3"] = "293.mat"
  # FE Outer race 0.007 inches centered @6:00
  matlab_files_name["FEOR.007@6_0"] = "294.mat"
  matlab_files_name["FEOR.007@6_1"] = "295.mat"
  matlab_files_name["FEOR.007@6_2"] = "296.mat"
  matlab_files_name["FEOR.007@6_3"] = "297.mat"
  # FE Outer race 0.007 inches centered @3:00
  matlab_files_name["FEOR.007@3_0"] = "298.mat"
  matlab_files_name["FEOR.007@3_1"] = "299.mat"
  matlab_files_name["FEOR.007@3_2"] = "300.mat"
  matlab_files_name["FEOR.007@3_3"] = "301.mat"
  # FE Outer race 0.007 inches centered @12:00
  matlab_files_name["FEOR.007@12_0"] = "302.mat"
  matlab_files_name["FEOR.007@12_1"] = "305.mat"
  matlab_files_name["FEOR.007@12_2"] = "306.mat"
  matlab_files_name["FEOR.007@12_3"] = "307.mat"
  # FE Outer race 0.014 inches centered @3:00
  matlab_files_name["FEOR.014@3_0"] = "310.mat"
  matlab_files_name["FEOR.014@3_1"] = "309.mat"
  matlab_files_name["FEOR.014@3_2"] = "311.mat"
  matlab_files_name["FEOR.014@3_3"] = "312.mat"
  # FE Outer race 0.014 inches centered @6:00
  matlab_files_name["FEOR.014@6_0"] = "313.mat"
  # FE Outer race 0.021 inches centered @6:00
  matlab_files_name["FEOR.021@6_0"] = "315.mat"
  # FE Outer race 0.021 inches centered @3:00
  matlab_files_name["FEOR.021@3_1"] = "316.mat"
  matlab_files_name["FEOR.021@3_2"] = "317.mat"
  matlab_files_name["FEOR.021@3_3"] = "318.mat"
  # DE Inner Race 0.028 inches
  matlab_files_name["DEIR.028_0"] = "3001.mat"
  matlab_files_name["DEIR.028_1"] = "3002.mat"
  matlab_files_name["DEIR.028_2"] = "3003.mat"
  matlab_files_name["DEIR.028_3"] = "3004.mat"
  # DE Ball 0.028 inches
  matlab_files_name["DEB.028_0"] = "3005.mat"
  matlab_files_name["DEB.028_1"] = "3006.mat"
  matlab_files_name["DEB.028_2"] = "3007.mat"
  matlab_files_name["DEB.028_3"] = "3008.mat"
  return matlab_files_name

def get_tensors_from_matlab(matlab_files_name, rawfilesdir=""):
  """
  Extracts the acquisitions of each Matlab file in the dictionary matlab_files_name.
  """
  acquisitions = {}
  for key in matlab_files_name:
    file_name = os.path.join(rawfilesdir, matlab_files_name[key])
    matlab_file = scipy.io.loadmat(file_name)
    for position in ['DE','FE', 'BA']:
      keys = [key for key in matlab_file if key.endswith(position+"_time")]
      if len(keys)>0:
        array_key = keys[0]
        acquisitions[key+position.lower()] = matlab_file[array_key].reshape(1,-1)[0]
  return acquisitions
