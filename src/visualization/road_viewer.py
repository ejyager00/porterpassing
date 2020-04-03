import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import shapefile

def get_centerline_data(dir="data/raw/Road_Centerlines/RoadExport"):
    with shapefile.Reader(dir) as sf:
        return sf.shapes()

xmin = 999999999999999999999999
ymin = 999999999999999999999999
xmax = -999999999999999999999999
ymax = -999999999999999999999999
for polyline in get_centerline_data():
    for point in polyline.points:
        if point[0]<xmin:
            xmin=point[0]
        if point[0]>xmax:
            xmax=point[0]
        if point[1]<ymin:
            ymin=point[1]
        if point[1]>ymax:
            ymax=point[1]
fig, ax = plt.subplots()
for polyline in get_centerline_data():
    verts = polyline.points
    codes = [Path.MOVETO] + [Path.LINETO]*(len(polyline.points)-1)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='white', lw=2)
    ax.add_patch(patch)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
plt.show()
