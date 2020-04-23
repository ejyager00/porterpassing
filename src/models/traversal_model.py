import pickle
from numpy import NaN
from numpy import isnan
import sys

DISTANCE_AHEAD = 300
HEIGHT_DIFF = 3.5

def distance(x1,y1,x2,y2):
    return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**.5

def check_arguments(args):
    if len(args)<2:
        raise RuntimeError("You must include two pickle files in the arguments.")

def main(args):

    heights=pickle.load(open(args[0], 'rb')) #'data/interim/centerpoints.pickle'

    roads=[]
    for road in heights:
        r=[]
        for i, point in enumerate(road):
            if isnan(point[2]):
                r.append([False,False])
                continue
            p = []
            dif=1
            dist=0
            while True:
                if i+dif==len(road):
                    p.append(False)
                    break
                else:
                    dist+= distance(road[i+dif][0],road[i+dif][1],road[i+dif-1][0],road[i+dif-1][1])
                    if isnan(road[i+dif][2]):
                        p.append(False)
                        break
                    elif road[i+dif][2]-point[2]>=HEIGHT_DIFF:
                        p.append(False)
                        break
                    elif dist>DISTANCE_AHEAD:
                        p.append(True)
                        break
                dif+=1
            dif=-1
            dist=0
            while True:
                if i+dif==-1:
                    p.append(False)
                    break
                else:
                    dist+= distance(road[i+dif][0],road[i+dif][1],road[i+dif+1][0],road[i+dif+1][1])
                    if isnan(road[i+dif][2]):
                        p.append(False)
                        break
                    elif road[i+dif][2]-point[2]>=HEIGHT_DIFF:
                        p.append(False)
                        break
                    elif dist>DISTANCE_AHEAD:
                        p.append(True)
                        break
                dif-=1
            r.append(p)
        roads.append(r)

    with open(args[1], 'wb') as pickle_file: #'data/processed/zones.pickle'
        pickle.dump(roads, pickle_file)

if __name__=='__main__':
    #args: centerpoints_pickle zones_pickle
    check_arguments(sys.argv[1:])
    main(sys.argv[1:])
