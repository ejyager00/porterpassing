import shapefile
import csv

class RoadBin:

    def __init__(self, start_point, end_point, height):
        self.start_point = start_point
        self.end_point = end_point
        self.height = height

def get_centerline_data(dir="data/interim/centerlines"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

def get_elevations():
    with open("road_points.csv","r") as points_file:
        
    return

def create_road_bins(road):
    return

def calculate_roadbin_height(roadbins, elevations):
    return

roads = get_centerline_data()
for road in roads:
    road_bins = create_road_bins(road)
    road_bins = calculate_roadbin_height(road_bins, elevations)
