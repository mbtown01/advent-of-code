import numpy as np


def updateVisibleFromLeftToRight(treeGrid: np.array, isVisibleGrid: np.array):
    height, width = treeGrid.shape
    for j in range(height):
        minValue = treeGrid[j][0]
        for i in range(width):
            if treeGrid[j][i] > minValue:
                isVisibleGrid[j][i] = 1
                minValue = treeGrid[j][i]


def countVisibleFromLeftToRight(treeGrid: np.array):
    height, width = treeGrid.shape
    numVisibleGrid = treeGrid * 0
    for j in range(height):
        for i in range(width-1):
            for i2 in range(i+1, width):
                numVisibleGrid[j][i] += 1
                if treeGrid[j][i] <= treeGrid[j][i2]:
                    break
    return numVisibleGrid


with open('2022/day8.txt') as reader:
    inputGrid = list(list(int(b) for b in a.strip())
                     for a in reader.readlines())

width, height = len(inputGrid[0]), len(inputGrid)
treeGrid = np.array(inputGrid, dtype=np.int32)
isVisibleGrid = np.ones([height, width], dtype=np.int32)
isVisibleGrid[1:height-1, 1:width-1] = 0

updateVisibleFromLeftToRight(treeGrid, isVisibleGrid)
numVisibleGrid = countVisibleFromLeftToRight(treeGrid)
grids = (treeGrid, isVisibleGrid, numVisibleGrid)

grids = list(a[:, ::-1] for a in grids)
updateVisibleFromLeftToRight(grids[0], grids[1])
grids[2] *= countVisibleFromLeftToRight(grids[0])

grids = list(a[:, ::-1].transpose() for a in grids)
updateVisibleFromLeftToRight(grids[0], grids[1])
grids[2] *= countVisibleFromLeftToRight(grids[0])

grids = list(a[:, ::-1] for a in grids)
updateVisibleFromLeftToRight(grids[0], grids[1])
grids[2] *= countVisibleFromLeftToRight(grids[0])

# grids = list(a[:, ::-1].transpose() for a in grids)
print(f"part 1: {grids[1].sum()}")
print(f"part 2: {grids[2].max()}")
