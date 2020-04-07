import shapefile
import pickle
#from numpy import genfromtxt

def get_centerline_data(dir="data/interim/centerlines"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

#def get_lidar_points(file="data/interim/road_points.csv"):
#    return genfromtxt(file, delimiter=',')

def generate_bins(road):
    rdpts=road.points
    segments=[]
    for i in range(1,len(rdpts)):
        dx = rdpts[i][0]-rdpts[i-1][0]
        dy = rdpts[i][1]-rdpts[i-1][1]
        magnitude = (dx*dx+dy*dy)**.5
        if magnitude == 0:
            continue
        dx=dx/magnitude
        dy=dy/magnitude
        curx = rdpts[i-1][0]
        cury = rdpts[i-1][1]
        iterations=int(magnitude/2)
        if magnitude%2<1:
            iterations-=1
            if iterations<0:
                diff = 1-magnitude
                curx = curx - diff*dx
                cury = cury - diff*dy
        bins=[]
        while iterations>0:
            corners=[]
            corners.append((curx-10*dy,cury+10*dx))
            corners.append((curx+10*dy,cury-10*dx))
            curx = curx + 2*dx
            cury = cury + 2*dy
            corners.append((curx+10*dy,cury-10*dx))
            corners.append((curx-10*dy,cury+10*dx))
            bins.append(corners)
            iterations-=1
        corners=[]
        corners.append((curx-10*dy,cury+10*dx))
        corners.append((curx+10*dy,cury-10*dx))
        curx = rdpts[i][0]
        cury = rdpts[i][1]
        corners.append((curx+10*dy,cury-10*dx))
        corners.append((curx-10*dy,cury+10*dx))
        segments.append(bins)
    return segments

roads = get_centerline_data()
#points = get_lidar_points()

road_bins = []
for road in roads:
    road_bins.append(generate_bins(road))
with open("data/interim/roadbins.pickle", 'wb') as pickle_file:
    pickle.dump(road_bins, pickle_file)
