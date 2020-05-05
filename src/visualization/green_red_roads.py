import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import pickle
import sys

COLORS = ["red", "green"]
codes = [Path.MOVETO,Path.LINETO]

def main(args):
    zones = pickle.load(open("data/processed/zones.pickle","rb"))
    points = pickle.load(open("data/interim/centerpoints.pickle","rb"))

    fig, ax = plt.subplots()
    xmin=points[0][0][0]
    xmax=points[0][0][0]
    ymin=points[0][0][1]
    ymax=points[0][0][1]
    for i, road in enumerate(zones):
        current=road[0][0]
        last_point=points[i][0]
        for j, point in enumerate(road):
            if points[i][j][0]<xmin:
                xmin=points[i][j][0]
            if points[i][j][1]<ymin:
                ymin=points[i][j][1]
            if points[i][j][0]>xmax:
                xmax=points[i][j][0]
            if points[i][j][1]>ymax:
                ymax=points[i][j][1]
            if j==len(road)-1:
                verts = [[last_point[0],last_point[1]],[points[i][j][0],points[i][j][1]]]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='white', lw=2, color=COLORS[current])
                ax.add_patch(patch)
            elif point[0]!=current:
                verts = [[last_point[0],last_point[1]],[points[i][j][0],points[i][j][1]]]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='white', lw=2, color=COLORS[current])
                ax.add_patch(patch)
                current=road[j+1][0]
                last_point=points[i][j+1]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    plt.show()

    fig, ax = plt.subplots()
    for i, road in enumerate(zones):
        current=road[0][1]
        last_point=points[i][0]
        for j, point in enumerate(road):
            if j==len(road)-1:
                verts = [[points[i][j][0],points[i][j][1]],[last_point[0],last_point[1]]]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='white', lw=2, color=COLORS[current])
                ax.add_patch(patch)
            elif point[0]!=current:
                verts = [[points[i][j][0],points[i][j][1]],[last_point[0],last_point[1]]]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='white', lw=2, color=COLORS[current])
                ax.add_patch(patch)
                current=road[j+1][1]
                last_point=points[i][j+1]
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    plt.show()

if __name__=="__main__":
    main(sys.argv[1:])
