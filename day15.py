import numpy as np


class Node:

    def __init__(self, i: int, j: int, risk: int) -> None:
        self.i = i
        self.j = j
        self.risk = risk
        self.totalRisk = 99999
        self.visited = False

    def __repr__(self):
        return f"[{self.i},{self.j}] risk={self.risk} total={self.totalRisk}"


riskMatrix = list()
with open('day15.txt') as reader:
    for line in reader.readlines():
        riskMatrix.append(list(int(a) for a in line.strip()))

# Comment this out if we're not on part 2
newMatrix = list()
for tile_j in range(5):
    for j, row in enumerate(riskMatrix):
        newMatrix.append(list(
            (a+tile_i+tile_j-1) % 9+1 or 1 for tile_i in range(5) for a in row))
riskMatrix = newMatrix

# Build the larger matrix in [i, j] so we can address the nodes directly
# rather than each node having a list of it's adjacent nodes
allNodes, allNodeMatrix = list(), list()
nj, ni = len(riskMatrix), len(riskMatrix[0])
for j, row in enumerate(riskMatrix):
    nodeRow = list()
    allNodeMatrix.append(nodeRow)
    for i, risk in enumerate(row):
        node = Node(i, j, risk)
        nodeRow.append(node)

allNodes.append(allNodeMatrix[0][0])
allNodes[0].totalRisk = 0


while len(allNodes) > 0:
    allNodes.sort(key=lambda a: a.totalRisk)
    thisNode = allNodes.pop(0)
    thisNode.visited = True
    i, j = thisNode.i, thisNode.j

    adjacentNodes = list()
    if i + 1 < ni:
        adjacentNodes.append(allNodeMatrix[j][i+1])
    if i > 0:
        adjacentNodes.append(allNodeMatrix[j][i-1])
    if j + 1 < nj:
        adjacentNodes.append(allNodeMatrix[j+1][i])
    if j > 0:
        adjacentNodes.append(allNodeMatrix[j-1][i])

    for adjacentNode in adjacentNodes:
        adjacentNode.totalRisk = min(
            adjacentNode.totalRisk, thisNode.totalRisk + adjacentNode.risk)
        if not adjacentNode.visited and adjacentNode not in allNodes:
            allNodes.append(adjacentNode)


print(f"part 1: {allNodeMatrix[-1][-1]}")
