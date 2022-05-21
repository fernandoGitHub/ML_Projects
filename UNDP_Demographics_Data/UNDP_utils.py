import os
import shutil

def generate_file_list_from_dir(path, filter = '*.*', display=False):
  """generate_list_from_dir(path, filter = '*.*', display=False) returns two lists of strings.
  The first includes the names of the csv files, the second the full paths. The filter parameter
  can be used to return only a given type of files.
  By default, the function doesn't filter any file"""

  file_list = os.listdir(path=path)

  if filter != '*.*':
    file_list = [file for file in file_list if filter in file]

  full_path_list = [os.path.join(path, file) for file in file_list]

  if display:
    print(file_list)

  return file_list, full_path_list


