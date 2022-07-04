#!/usr/bin/env python3

# BetterUp Data: Goals

# 1. Look for `survey.csv` in each of the `.zip` files.
# 2. Append directory name to each of the `survey.csv` files.
# 3. Put all of the `directory-name-survey.csv` files into a new directory.
# 4. Merge all `directory-name-survey.csv` files into one `merged-survey.csv` file.

#import libraries
import os
import glob
import zipfile
import shutil
from os import walk, path, rename
import pandas as pd
from pathlib import Path

#### Set parent directory

parent_directory = os.getcwd()

## message
print('## Please wait while the script is processing...')

#### extract survey.csv files from the .zip files

print('## Now extracting all .csv files from .zip files...')

zip_extension = ".zip" # file extension we are looking for
print('')
print('## List of all .zip files in this folder:')
print('')

for item in os.listdir(): # loop through items in dir
    if not item.startswith('.'):
        if item.endswith(zip_extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            print(file_name) # print all the .zip files
            with zipfile.ZipFile(file_name) as zipObject:
                listOfFileNames = zipObject.namelist()
                for fileName in listOfFileNames:
                    if fileName.endswith('survey.csv'): #look only for .csv files
                        zipObject.extract(fileName, 'temp_survey') # put .csv files in new folder

print('')
print('## All .csv files were extracted successfully to temp_survey folder')

#### get rid of __MACOSX folder
parent_directory = os.getcwd() # set parent directory

# path to the unneeded __MACOSX folder
mac_path = os.path.join(parent_directory, 'temp_survey/__MACOSX')

# delete the __MACOSX folder
try:
    shutil.rmtree(mac_path)
except OSError as e:
    print("Error: %s : %s" % (mac_path, e.strerror))

#### append the directory name to the survey.csv files

print('## Now renaming .csv files with folder names...')

for dirpath, _, files in walk('temp_survey'):
    for f in files:
        rename(path.join(dirpath, f), path.join(dirpath, path.split(dirpath)[-1] + '_' + f))

print('')
print('## All files below were created:')
print('')

# print all the newly create files to check labeled properly
for path, subdirs, files in walk('temp_survey'):
    for name in files:
        print(name)

print('')

#### make a new directory for the survey files
survey_files_dir = "survey_files"

# join new directory into the path
survey_path = os.path.join(parent_directory, survey_files_dir)

os.mkdir(survey_path) # make the directory

#### Move all of the directory-name-survey.csv files into new directory

# temporary directory
temp_dir = "temp_survey"

print('## Copying all survey files into survey_files directory...')
print('')

for root, dir, files in os.walk(temp_dir):
    for file in files:
        if "_survey.csv" in file: #check if it is a .csv files
            shutil.copy(os.path.join(root, file), survey_files_dir)
            print(file, 'copied successfully')
print('')

#### create a compiled .csv file of all the survey.csv files

print('## Copying all survey data into one .csv file...')

# change directory into survey_files
os.chdir(survey_path)

csv_extension = "csv"

# get all files that have the .zip extension (defined above)
all_filenames = [i for i in glob.glob('*.{}'.format(csv_extension))]

# combine all files in the list
compiled_survey_data = pd.concat([pd.read_csv(f) for f in all_filenames])

# export to .csv
compiled_survey_data.to_csv( "compiled_survey_data.csv", index=False, encoding='utf-8-sig')

print('## compiled_survey_data.csv file is now created.')
print('')

#### remove temp_survey folder

os.chdir(parent_directory) # change directory again

# path to the unneeded temp_survey folder

temp_path = os.path.join(parent_directory, 'temp_survey/')

# delete the temp_survey folder
try:
    shutil.rmtree(temp_path)
    print('## temp_survey folder is now deleted.')
except OSError as e:
    print("Error: %s : %s" % (mac_path, e.strerror))
print('')

#### make a directory for the final compiled .csv file

# make a new directory for the compiled survey file
compiled_survey_files_dir = "compiled_survey"

# join new directory into the path
compiled_survey_path = os.path.join(parent_directory, compiled_survey_files_dir)

os.mkdir(compiled_survey_files_dir) # make the directory

#### put compiled csv file into a new folder

# look for the compiled .csv file

file_source = survey_path
file_destination = compiled_survey_path

for file in Path(file_source).glob('compiled_survey_data.csv'):
    shutil.move(os.path.join(file_source,file),file_destination)
    print('## Success!')
    print('## compiled_survey_data.csv can be found in the compiled_survey folder.')
    print('## Individual surveys can be found in the survey_files folder.')
