from os import listdir
from os.path import isfile
import zipfile

files = [f for f in listdir() if isfile(f)]
for file in files:
     with zipfile.ZipFile(file) as zip_ref:
             zip_ref.extractall()