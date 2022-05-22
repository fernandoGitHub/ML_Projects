import os
import shutil

import numpy as np
import pandas as pd

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


# Helper Function to remove spaces and replace '..' with -1
def clean_data(df):
  # We need to remove spaces from the dataframe prior to interpolation
  # And also to replace the unknown values (expressed as two consecutive points)
  # to an arbitrary value of -1
  # Finally we will convert the values to float
  for col in df.columns:
    df[col] = df[col].astype(str).str.strip().replace('..','-1')

  return df


# Helper function to set the columns type
def set_column_type(df, type, inclusive=None, exclusive=None):

  cols = df.columns
  if inclusive == None:
    cols = [col for col in cols if not(col in exclusive)]
  else:
    cols = [col for col in cols if (col in inclusive)]

  for col in cols:
    df[col] = df[col].astype(float)

  return df


# Helper function to replace unknown values by mean values for that year
def replace_unknown_by_mean(df):
  for col in df.columns:
    if df[col].dtype == 'float64':
      mean_value = np.round(df[df[col] != -1][col].mean(), 1)
      df[col] = df[col].replace(-1.0, mean_value)
  
  return df


# Helper function to create interpolated columns
def interpolate_columns(df, new_cols):
  
  def interpolate (y1, y2, x1, x2, x):
    return np.round(y1 + (y2-y1)/(x2-x1) * (x-x1), 1)

  for col in new_cols:
    if not (col in df.columns):
      # Adding a new column and creating the interpolation
      year = int(col)
      prev_year = year - year % 5
      next_year = prev_year + 5

      df[col] = np.vectorize(interpolate)(df[str(prev_year)], df[str(next_year)], prev_year, next_year, year)

  sorted_df = df[['HDI Rank', 'Country']]
  for col in new_cols:
    sorted_df[col] = df[col]

  return sorted_df



