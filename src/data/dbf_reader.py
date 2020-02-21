import shapefile

sf = shapefile.Reader("data/raw/Road_Centerlines/RoadExport")
print(sf)
sf.shapeType
len(sf)
shapes = sf.shapes()
for s in shapes:
    print(s.points)
