rar_files_name = ["K001.rar","K002.rar","K003.rar","K004.rar","K005.rar","K006.rar",
                  "KA01.rar", "KA03.rar", "KA04.rar", "KA05.rar", "KA06.rar", "KA07.rar", 
                  "KA08.rar", "KA09.rar", "KA15.rar", "KA16.rar", "KA22.rar", "KA30.rar", 
                  "KB23.rar", "KB24.rar", "KB27.rar", 
                  "KI01.rar", "KI03.rar", "KI04.rar", "KI05.rar", "KI07.rar", "KI08.rar", 
                  "KI14.rar", "KI16.rar", "KI17.rar", "KI18.rar", "KI21.rar"]

import urllib.request
import os.path
def download_paderbornfiles(rar_files_name):
  url="http://groups.uni-paderborn.de/kat/BearingDataCenter/"
  n = len(rar_files_name)
  for i in rar_files_name:
    file_name = i
    if not os.path.exists(file_name):
      urllib.request.urlretrieve(url+file_name, file_name)
    print(file_name)

download_paderbornfiles(rar_files_name)
