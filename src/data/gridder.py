import os
from pathlib import Path
from laspy.file import File
import numpy as np
from scipy.interpolate import griddata
import pickle
from lidar_reader import total_las_points
from centerline_reader import get_centerlines

def gridder():
    centerlines = get_centerlines()
    print("center points found")
    desired = centerlines.pop()
    for x in centerlines:
        desired = desired.extend(x)
    print("desired points found")
    known = total_las_points()
    print("known points found")
    results = griddata(coords[:,0:2],coords[:,2],desired)
    print("resultant points found")

if __name__ == '__main__':
    gridder()
