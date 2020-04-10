import pickle
from numpy import genfromtxt
import numpy as np

def get_bins(file="data/interim/roadbins.pickle"):
    return pickle.load(open(file,'rb'))

def get_lidar_points(file="data/interim/road_points.csv"):
    return genfromtxt(file, delimiter=',')

def find_points_in_bin(pts,bin):
    points=[]
    dot1 = (bin[0][0]-bin[1][0])*(bin[0][0]-bin[1][0])+(bin[0][1]-bin[1][1])*(bin[0][1]-bin[1][1])
    dot2 = (bin[2][0]-bin[1][0])*(bin[2][0]-bin[1][0])+(bin[2][1]-bin[1][1])*(bin[2][1]-bin[1][1])
    for p in pts:
        pdot1 = (p[0]-bin[1][0])*(bin[0][0]-bin[1][0])+(p[1]-bin[1][1])*(bin[0][1]-bin[1][1])
        pdot2 = (p[0]-bin[1][0])*(bin[2][0]-bin[1][0])+(p[1]-bin[1][1])*(bin[2][1]-bin[1][1])
        if (pdot1>=0)and(pdot2>=0)and(pdot1<=dot1)and(pdot2<=dot2):
            points.append(p)
    return points

bins = get_bins()
points = get_lidar_points()
points = points[points[:,0].argsort()]

roads=[]
for i, road in enumerate(bins):
    segments=[]
    for j, segment in enumerate(road):
        bins=[]
        for k, bin in enumerate(segment):
            minX = bin[0][0]
            maxX = bin[0][0]
            for p in bin[1:]:
                if p[0]<minX:
                    minX=p[0]
                elif p[0]>maxX:
                    maxX=p[0]
            pts=points[points[:,0]<=maxX]
            pts=pts[pts[:,0]>=minX]
            bin_pts=find_points_in_bin(pts,bin)
            if len(bin_pts)>0:
                height=np.average(bin_pts)
            else:
                height=np.nan
            bins.append(height)
        segments.append(bins)
    roads.append(segments)
with open("data/interim/road_heighgts.pickle", 'wb') as pickle_file:
    pickle.dump(roads, pickle_file)
