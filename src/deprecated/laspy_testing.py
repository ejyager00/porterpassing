from laspy.file import File
import numpy as np

las_file = File('data/raw/in2018_29502285_12.las')

print('scale ' + str(las_file.get_header().get_scale()))
print('offset ' + str(las_file.get_header().get_offset()))
print(str(len(las_file.get_points()))+' points')
for dim in las_file.point_format:
    print(dim.name)
#for point in las_file.get_points():
#    print(point)
#las_file.visualize()
coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
found = []
for x in coords:
    if x[0] not in found:
        found.append(x[0])
        print(len(found))
print(len(found))
print(found)
#print(coords[1,1])

las_file.close()
