import shapefile
import pickle
import os
from laspy.file import File
import numpy as np
from shapely.geometry import LineString
import sys

def get_centerline_data(dir="data/raw/Road_Centerlines/RoadExport"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

def las_min_max(path='data/raw/', multi=False):
    las_file_names = []
    if multi:
        files = os.listdir(path)
        for filename in files:
            if filename[-4:]=='.las':
                las_file_names.append(path+filename)
    else:
        las_file_names.append(path)
    las_file = File(las_file_names[0])
    bounds = {
        'MIN_X':las_file.x[0],
        'MAX_X':las_file.x[0],
        'MIN_Y':las_file.y[0],
        'MAX_Y':las_file.y[0]
    }
    las_file.close()
    for filename in las_file_names:
        las_file = File(filename)
        coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
        minx=coords[:,0].min()
        maxx=coords[:,0].max()
        miny=coords[:,1].min()
        maxy=coords[:,1].max()
        if minx<bounds['MIN_X']:
            bounds['MIN_X']=minx
        if maxx>bounds['MAX_X']:
            bounds['MAX_X']=maxx
        if miny<bounds['MIN_Y']:
            bounds['MIN_Y']=miny
        if maxy>bounds['MAX_Y']:
            bounds['MAX_Y']=maxy
        las_file.close()
    return bounds

def is_in_bounds(p, b):
    return ((p[0]>=b['MIN_X']) and (p[0]<=b['MAX_X'])) and ((p[1]>=b['MIN_Y']) and (p[1]<=b['MAX_Y']))

def line_seg_intersect(line1, line2):
    x1=line1[0][0]
    x2=line1[1][0]
    x3=line2[0][0]
    x4=line2[1][0]
    y1=line1[0][1]
    y2=line1[1][1]
    y3=line2[0][1]
    y4=line2[1][1]
    try:
        t1 = ((y3-y4)*(x1-x3)+(x4-x3)*(y1-y3))/((x4-x3)*(y1-y2)-(x1-x2)*(y4-y3))
        t2 = ((y1-y2)*(x1-x3)+(x2-x1)*(y1-y3))/((x4-x3)*(y1-y2)-(x1-x2)*(y4-y3))
    except ZeroDivisionError:
        return False
    if t1>=0 and t1<=1 and t2>=0 and t2<=1:
        return (x1+t1*(x2-x1),y1+t1*(y2-y1))
    else:
        return False

def boundary_intersect(p1, p2, b):
    bounds = ((b['MIN_X'],b['MIN_Y']),(b['MIN_X'],b['MAX_Y']),(b['MAX_X'],b['MAX_Y']),(b['MAX_X'],b['MIN_Y']))
    intersections = []
    for i in range(4):
        intersect = line_seg_intersect((bounds[i-1],bounds[i]), (p1, p2))
        if intersect!=False:
            intersections.append(intersect)
    if len(intersections)==0:
        return False
    elif len(intersections)==1:
        return intersections[0]
    else:
        return intersections

def get_relevant_centerlines(centerlines, bounds):
    inbound_roads = []
    for polyline in centerlines:
        polyline=polyline.points
        new_points = []
        if is_in_bounds(polyline[0], bounds):
            new_points.append(polyline[0])
        for i in range(1, len(polyline)):
            if is_in_bounds(polyline[i-1], bounds) and is_in_bounds(polyline[i], bounds):
                new_points.append(polyline[i])
            elif is_in_bounds(polyline[i-1], bounds):
                new_points.append(boundary_intersect(polyline[i-1], polyline[i], bounds))
                inbound_roads.append(new_points)
                new_points = []
            elif is_in_bounds(polyline[i], bounds):
                new_points.append(boundary_intersect(polyline[i-1], polyline[i], bounds))
                new_points.append(polyline[i])
            elif boundary_intersect(polyline[i-1], polyline[i], bounds)!= False:
                inbound_roads.append(boundary_intersect(polyline[i-1], polyline[i], bounds))
        if len(new_points)>1:
            inbound_roads.append(new_points)
    return inbound_roads

def check_arguments(args):
    if len(args)<4:
        raise RuntimeError("You must include a shapefile, the number of las files, a path for las files, and a path to save new shapefile.")
    try:
        int(args[1])
    except:
        raise RuntimeError("Second argument must be the number of las files.")
    try:
        shapefile.Reader(args[0])
    except:
        raise RuntimeError("First argument must be a shapefile.")

def main(args):
    check_arguments(args)
    centerlines=get_centerline_data(args[0])
    bounds=las_min_max(args[2],int(args[1])>1)
    relevant_centerlines = get_relevant_centerlines(centerlines, bounds)
    with shapefile.Writer(args[3],shapeType=3) as shp:
        shp.field("TEMP",'N')
        for i,line in enumerate(relevant_centerlines):
            shp.shape(LineString(line))
            shp.record(i)

if __name__=='__main__':
    #args: shapefile number_of_las_files path shapefile
    main(sys.argv[1:])
