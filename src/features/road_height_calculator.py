import pickle
import numpy as np
import sys
from laspy.file import File
import os

def get_bins(file="data/interim/roadbins.pickle"):
    return pickle.load(open(file,'rb'))

def get_lidar_points(path='data/raw/', multi=False):
    las_file_names = []
    if multi:
        files = os.listdir(path)
        for filename in files:
            if filename[-4:]=='.las':
                las_file_names.append(path+filename)
    else:
        las_file_names.append(path)
    las_file = File(las_file_names.pop(0))
    coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
    las_file.close()
    for filename in las_file_names:
        las_file = File(filename)
        coords = np.concatenate((coords, np.vstack((las_file.x, las_file.y, las_file.z)).transpose()), axis=0)
        las_file.close()
    return coords

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

def main(args):
    bins = get_bins(args[0])
    points = get_lidar_points(args[2],int(args[1])>1)
    #points = points[points[:,0].argsort()]

    roads=[]
    for i, road in enumerate(bins):
        segments=[]
        for j, segment in enumerate(road):
            bins=[]
            for k, bin in enumerate(segment):
                minX = bin[0][0]
                maxX = bin[0][0]
                minY = bin[0][1]
                maxY = bin[0][1]
                for p in bin[1:]:
                    if p[0]<minX:
                        minX=p[0]
                    elif p[0]>maxX:
                        maxX=p[0]
                    if p[1]<minY:
                        minY=p[1]
                    elif p[1]>maxY:
                        maxY=p[1]
                pts=points[points[:,0]<=maxX]
                pts=pts[pts[:,0]>=minX]
                #pts=pts[pts[:,1].argsort()]
                pts=pts[pts[:,1]<=maxY]
                pts=pts[pts[:,1]>=minY]
                bin_pts=find_points_in_bin(pts,bin)
                if len(bin_pts)>0:
                    height=np.mean(bin_pts, axis=0)[2]
                else:
                    height=np.nan
                bins.append(height)
            segments.append(bins)
        roads.append(segments)
    with open(args[3], 'wb') as pickle_file:
        pickle.dump(roads, pickle_file)

if __name__ == '__main__':
    #args: bin_pickle number_of_las_files path out
    main(sys.argv[1:])
