import pickle
from numpy import NaN
from numpy import isnan

DISTANCE_AHEAD = 100
HEIGHT_DIFF = 3.5

def distance(x1,y1,x2,y2):
    return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**.5

heights=pickle.load(open('data/interim/centerpoints.pickle', 'rb'))

roads=[]
for road in heights:
    r=[]
    for i, point in enumerate(road):
        if isnan(point[2]):
            r.append([False,False])
            continue
        p = []
        dif=1
        distance=0
        while True:
            distance+= distance(road[i+dif][0],road[i+dif][1],road[i+dif-1][0],road[i+dif-1][1])
            if i+dif==len(road):
                p.append(False)
                break
            elif isnan(road[i+dif][2]):
                p.append(False)
                break
            elif road[i+dif][2]-point[2]>=HEIGHT_DIFF:
                p.append(False)
                break
            elif distance>DISTANCE_AHEAD:
                p.append(True)
                break
            dif+=1
        dif=-1
        while True:
            distance+= distance(road[i+dif][0],road[i+dif][1],road[i+dif+1][0],road[i+dif+1][1])
            if i+dif==-1:
                p.append(False)
                break
            elif isnan(road[i+dif][2]):
                p.append(False)
                break
            elif road[i+dif][2]-point[2]>=HEIGHT_DIFF:
                p.append(False)
                break
            elif distance>DISTANCE_AHEAD:
                p.append(True)
                break
            dif-=1
        r.append(p)
    roads.append(r)

with open('data/processed/zones.pickle', 'wb') as pickle_file:
    pickle.dump(roads, pickle_file)
