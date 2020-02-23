import shapefile

def get_centerlines(dir="data/raw/Road_Centerlines/RoadExport"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

if __name__ == '__main__':
    get_centerlines()
