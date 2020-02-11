from laspy.file import File
import numpy as np

las_file = File('data/raw/in2018_29502285_12.las')
#las_file.open()


#for x in las_file.get_points():
#    print(x)

print(len(las_file.get_points()))
print(las_file.get_points()[0])
coords = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()
for x in coords:
    print(x)

las_file.close()
