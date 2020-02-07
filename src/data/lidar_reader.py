import os
from laspy.file import File
import numpy as np

files = os.listdir('data/raw/')
las_file_names = []
for filename in files:
    if filename[-4:]=='.las':
        las_file_names.append(filename)
