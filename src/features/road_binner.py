import shapefile
import pickle
import sys

DEFAULT_BIN_LENGTH=5

def get_centerline_data(dir="data/interim/centerlines"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

def generate_bins(road, bin_length):
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
        iterations=int(magnitude/bin_length)
        if magnitude%bin_length<bin_length*.65:
            iterations-=1
            if iterations<0:
                diff = bin_length*.65-magnitude
                curx = curx - diff*dx
                cury = cury - diff*dy
        bins=[]
        while iterations>0:
            corners=[]
            corners.append((curx-10*dy,cury+10*dx))
            corners.append((curx+10*dy,cury-10*dx))
            curx = curx + 6*dx
            cury = cury + 6*dy
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

def check_arguments(args):
    if len(args)<2:
        raise RuntimeError("You must include a shapefile and a pickle file in the arguments.")
    else
        try:
            shapefile.Reader(args[0])
        except:
            raise RuntimeError("The first argument should be a shapefile.")
        try:
            if (args[1][-7:]!=".pickle"):
                raise RuntimeError("The second argument should be a pickle file.")
        except:
            raise RuntimeError("The second argument should be a pickle file.")
        if len(args)>2:
            try:
                float(args[2])
            except:
                raise RuntimeError("The third argument should be a number.")

def main(args):
    check_arguments(args)
    if len(args)<3:
        bin_length=DEFAULT_BIN_LENGTH
    else:
        bin_length=float(args[2])
    roads = get_centerline_data(args[0])

    road_bins = []
    for road in roads:
        road_bins.append(generate_bins(road, bin_length))
    with open(args[1], 'wb') as pickle_file:
        pickle.dump(road_bins, pickle_file)

if __name__ == '__main__':
    main(sys.argv[1:])
