import os
from laspy.file import File
import numpy as np
from scipy.interpolate import LinearNDInterpolator
import pickle

def create_interpolator(dir='data/raw/',dumpfile='linear_interpolator.pickle'):
    files = os.listdir(dir)
    las_file_names = []
    for filename in files:
        if filename[-4:]=='.las':
            las_file_names.append(filename)
    las_file = File(dir+las_file_names.pop(0))
    coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
    las_file.close()
    for filename in las_file_names:
        las_file = File(dir+filename)
        coords = np.concatenate((coords, np.vstack((las_file.x, las_file.y, las_file.z)).transpose()), axis=0)
        las_file.close()
    interpolator = LinearNDInterpolator(coords[:,0:2], coords[:,2])
    with open(dumpfile, 'wb') as pickle_file:
        pickle.dump(interpolator, pickle_file)
    return interpolator

if __name__ == '__main__':
    create_interpolator()
