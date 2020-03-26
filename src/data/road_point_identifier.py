from laspy.file import File
import shapefile
import os
import numpy as np

def get_centerline_data(dir="data/interim/centerlines"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

def distance_to_road(point, road):
    road=road.points
    p=point
    for i in range(1,len(road)):
        dx = road[i][0]-road[i-1][0]
        dy= road[i][1]-road[i-1][1]
        if dx==0 and dy==0:
            dx=p[0]-road[i][0]
            dy=p[1]-road[i][1]
            return (dx*dx+dy*dy)**.5
        t = ((p[0]-road[i-1][0])*dx+(p[1]-road[i-1][1])*dy)/(dx*dx+dy*dy)
        if t < 0 or t > 1:
            return 99999 #arbitrarily large constant
        else:
            dx = p[0]-road[i-1][0]+t*dx
            dy = p[1]-road[i-1][1]+t*dy
            return (dx*dx+dy*dy)**.5

centerlines = get_centerline_data()

files = os.listdir('data/raw/')
las_file_names = []
for filename in files:
    if filename[-4:]=='.las':
        las_file_names.append(filename)

road_points = []

for filename in las_file_names:
    las_file = File('data/raw/'+filename)
    coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
    for point in coords:
        for road in centerlines:
            if distance_to_road(point, road)<10:
                road_points.append(point)
                break
    las_file.close()
    print("another one down")

print(road_points)