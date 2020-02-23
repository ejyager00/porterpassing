import os
from laspy.file import File
import numpy as np
from scipy.interpolate import LinearNDInterpolator
import pickle

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
interpolator = LinearNDInterpolator(coords[:,0:2], coords[:,2])
with open('linear_interpolator.pickle', 'wb') as pickle_file:
    pickle.dump(interpolator, pickle_file)
