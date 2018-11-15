''' 
This script removes a few prefixes if they appear in the file name
An assumption here is that the prefix appears in the begining on the file name
'''

import os
from os import listdir
from os.path import isfile

PREFIXES_TO_REMOVE = [
  'Photonify - ',
  'Photonify-'
]

files = [f for f in listdir() if isfile(f)]
for file in files:
  for prefix in PREFIXES_TO_REMOVE:
    if file.find(prefix) != -1:
      newName = file.split(prefix)[-1]
      os.rename(file, newName)
      