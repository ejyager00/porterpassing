import os
from laspy.file import File
import numpy as np
from scipy.interpolate import SmoothBivariateSpline

files = os.listdir('data/raw/')
las_file_names = []
for filename in files:
    if filename[-4:]=='.las':
        las_file_names.append(filename)

las_file = File('data/raw/'+las_file_names.pop(0))
coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
las_file.close()
for filename in las_file_names:
    las_file = File('data/raw/'+filename)
    coords = np.concatenate((coords, np.vstack((las_file.x, las_file.y, las_file.z)).transpose()), axis=0)
    las_file.close()
coords_split = np.hsplit(coords, np.array([1,2]))
SmoothBivariateSpline(coords_split[0],coords_split[1],coords_split[2])
