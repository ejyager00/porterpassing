import shapefile
import pickle

def get_centerline_data(dir="data/raw/Road_Centerlines/RoadExport"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

def line_points(x1,y1,x2,y2):
	points=[]
	if x1==x2:
		if y2<y1:
			a=y2
			y2=y1
			y1=a
		points.append([x1,y1])
		while points[-1][1]<y2:
			points.append((x1, points[-1][1]+1))
		return points
	elif y1==y2:
		if x2<x1:
			a=x2
			x2=x1
			x1=a
		points.append([x1,y1])
		while points[-1][0]<x2:
			points.append((points[-1][0]+1, y1))
		return points
	dy = y2-y1
	dx = x2-x1
	length = ((x1-x2)**2+(y1-y2)**2)**.5
	dy = dy/length
	dx = dx/length
	length = int(length)
	for i in range(length+2):
		points.append([x1+i*dx,y1+i*dy])
	return points

def get_centerlines(dir="data/raw/Road_Centerlines/RoadExport",dumpfile='centerpoints.pickle',dump=False):
    shapes = get_centerline_data(dir)
    full_lines = []
    for shape in shapes:
        for i in range(1,len(shape.points)):
            full_lines.append(line_points(shape.points[i-1][0],shape.points[i-1][1],
                                          shape.points[i][0],shape.points[i][1]))
    if dump:
        with open(dumpfile, 'wb') as pickle_file:
            pickle.dump(full_lines, pickle_file)
    return full_lines

if __name__ == '__main__':
    get_centerlines(dump=True)
