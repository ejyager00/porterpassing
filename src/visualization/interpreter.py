import pickle
import numpy as np
import sys

PI=3.14159265
DIRECTIONS=("Northeast","North","Northwest","West","Southwest","South","Southeast","East")

def get_direction(x1,y1,x2,y2):
    x=x2-x1
    y=y2-y1
    if (not x) and (not y):
        return "From"
    angle = np.arccos(x/((x*x+y*y)**.5))
    angle = ((angle*(4/PI))-.5)%8
    return DIRECTIONS[int(angle)] + " from"

def text_builder(x1,y1,x2,y2,passing):
    string=get_direction(x1,y1,x2,y2)
    string+=" ("+str(x1)+","+str(y1)+") to (" + str(x2)+","+str(y2)+") should be "
    string+="no passing."*(not passing) + "passing."*passing + "\n"
    return string

def main(args):
    zones = pickle.load(open("data/processed/zones.pickle","rb"))
    points = pickle.load(open("data/interim/centerpoints.pickle","rb"))
    text = []
    for i, road in enumerate(zones):
        current=road[0][0]
        last_point=points[i][0]
        for j, point in enumerate(road):
            if j==len(road)-1:
                text.append(text_builder(last_point[0],last_point[1],points[i][j][0],points[i][j][1],current))
            elif point[0]!=current:
                text.append(text_builder(last_point[0],last_point[1],points[i][j][0],points[i][j][1],current))
                current=road[j+1][0]
                last_point=points[i][j+1]
        current=road[0][1]
        last_point=points[i][0]
        for j, point in enumerate(road):
            if j==len(road)-1:
                text.append(text_builder(points[i][j][0],points[i][j][1],last_point[0],last_point[1],current))
            elif point[1]!=current:
                text.append(text_builder(points[i][j][0],points[i][j][1],last_point[0],last_point[1],current))
                current=road[j+1][1]
                last_point=points[i][j+1]
    with open("data/processed/suggestions.txt","w") as outfile:
        outfile.writelines(text)

if __name__=="__main__":
    main(sys.argv[1:])
