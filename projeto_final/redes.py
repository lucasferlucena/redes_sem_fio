import package as pk
import router as node
import numpy as np
from scipy.spatial import distance
import copy

count = 0
nos = []
for x in range(3):
    for y in range(3):
        nos.append(node.Router(count, x, y))
        count = count +1

nos = np.array(nos)

pkg0 = pk.Package(0, 0, 10, [1,1,1,1,1], "DATA")
pkg1 = pk.Package(10, 3, 8, [1,1,2,2,1], "DATA")

for i in nos:
    i.findNeighbors(i.id, nos)

nos[0].networkSend(pkg0,nos)
#nos[3].networkSend(pkg1,nos)