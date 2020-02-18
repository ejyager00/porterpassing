from laspy.file import File
import numpy as np
import pandas as pd


las_file = File('data/raw/in2018_29502285_12.las')

print('scale ' + str(las_file.get_header().get_scale()))
print('offset ' + str(las_file.get_header().get_offset()))
print(str(len(las_file.get_points()))+' points')
for dim in las_file.point_format:
    print(dim.name)
#for point in las_file.get_points():
#    print(point)
#las_file.visualize()
coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
#print(coords)
#print(type(coords))
#coords = coords[coords[:,1].argsort()]
#coords = coords[coords[:,0].argsort(kind='mergesort')]
df = pd.DataFrame(coords, columns=['x','y','z'])
print(df.head())
print("xmin",df['x'].min())
print("xmax",df['x'].max())
print("xmin",df['y'].min())
print("xmax",df['y'].max())
las_file.close()

def discretize_las(coords, dim=(5000,5000)):
    df = pd.DataFrame(coords, columns=['x','y','z'])
    xmin = df['x'].min()
    xmax = df['x'].max()
    ymin = df['y'].min()
    ymax = df['y'].max()
    del df
    np.zeros(shape=dim)
