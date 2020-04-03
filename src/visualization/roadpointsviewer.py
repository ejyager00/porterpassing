import matplotlib.pyplot as plt
import csv

x = []
y = []
with open('data/interim/road_points.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for point in csvreader:
        x.append(point[0])
        y.append(point[1])

plt.scatter(x, y)
plt.show()
