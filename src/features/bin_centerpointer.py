import pickle

def get_centerpoint(bin):
    return ((bin[0][0]+bin[1][0]+bin[2][0]+bin[3][0])/4, (bin[0][1]+bin[1][1]+bin[2][1]+bin[3][1])/4)

bins=pickle.load(open('data/interim/bin.pickle', 'rb'))
heights=pickle.load(open('data/interim/heights.pickle', 'rb'))

roads=[]
for road in bins:
    segemnts=[]
    for segment in road:
        points=[]
        for bin in segment:
            points.append(get_centerpoint(bin))
        segments.append(points)
    roads.append(segments)

r = []
for i,road in enumerate(roads):
    p = []
    for j,segment in enumerate(road):
        for k, point in enumerate(segment):
            p.append((point[0],point[1],heights[i][j][k]))
    r.append(p)
roads = r

with open('data/interim/centerpoints.pickle', 'wb') as pickle_file:
    pickle.dump(roads, pickle_file)
