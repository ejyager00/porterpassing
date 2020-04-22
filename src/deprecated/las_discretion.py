from laspy.file import File
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

def discretize_las(coords, dim=(5000,5000)):
    df = pd.DataFrame(coords, columns=['x','y','z'])
    xmin = df['x'].min()
    xmax = df['x'].max()
    ymin = df['y'].min()
    ymax = df['y'].max()
    del df
    grid_x, grid_y = np.mgrid[xmin:xmax:5000j, ymin:ymax:5000j]
    points = coords[:,0:2]
    values = coords[:,2]
    grid = griddata(points, values, (grid_x, grid_y), method='linear')
    return grid


las_file = File('data/raw/in2018_29502285_12.las')

print('scale ' + str(las_file.get_header().get_scale()))
print('offset ' + str(las_file.get_header().get_offset()))
print(str(len(las_file.get_points()))+' points')
point_format = las_file.point_format
formatting = ""
for x in point_format:
    formatting += x + " "
print(formatting)
#las_file.visualize()
coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
print(discretize_las(coords))

las_file.close()
