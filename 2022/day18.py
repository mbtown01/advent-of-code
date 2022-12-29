from enum import Enum
from collections import defaultdict
import numpy as np


class Face:

    class Direction(Enum):
        POS_X, POS_Y, POS_Z = 0, 1, 2

    def __init__(self, loc: tuple, direction) -> None:
        self.loc = loc
        self.direction = direction

    def __repr__(self) -> str:
        return f"[Face {self.loc} {self.direction}]"

    def __hash__(self) -> int:
        return hash((*self.loc, self.direction))

    def __eq__(self, other: object) -> bool:
        return self.loc == other.loc and self.direction == other.direction


class Cube:

    def __init__(self, loc: tuple) -> None:
        self.loc = loc
        self.faceList = list()

        x, y, z = loc
        self.faceList.append(Face((x, y, z), Face.Direction.POS_X))
        self.faceList.append(Face((x, y, z), Face.Direction.POS_Y))
        self.faceList.append(Face((x, y, z), Face.Direction.POS_Z))
        self.faceList.append(Face((x+1, y, z), Face.Direction.POS_X))
        self.faceList.append(Face((x, y+1, z), Face.Direction.POS_Y))
        self.faceList.append(Face((x, y, z+1), Face.Direction.POS_Z))

    def __repr__(self) -> str:
        return f"[Cube {self.loc}]"


faceList, cubeList = list(), list()
minLoc, maxLoc = (1000, 1000, 1000), (-1000, -1000, -1000)
with open('2022/day18.txt') as reader:
    for line in reader.readlines():
        cube = Cube(tuple(int(a) for a in line.strip().split(',')))
        minLoc = tuple(min(a, b) for (a, b) in zip(minLoc, cube.loc))
        maxLoc = tuple(max(a, b+2) for (a, b) in zip(maxLoc, cube.loc))
        cubeList.append(cube)
        faceList += cube.faceList

faceMap = defaultdict(int)
for face in faceList:
    faceMap[face] += 1
exteriorFaces = list(a for (a, b) in faceMap.items() if b == 1)
print(f"part 1: {len(exteriorFaces)}")

# Build a 3D cube of zeros and ones, where a 1 represents the location
# of a solid cube
updates, cubeLocations = 1, np.zeros(maxLoc, dtype=np.int8)
for cube in cubeList:
    cubeLocations[cube.loc] = 1

# Iteratively scan the entire cube for cells that are 0 AND are either
# a) touching the edge of the world OR b) touching another 2 cell.  Once
# we have an iteration that change no 0 values to 2, we have found all the
# exterior cells, and know that remaining 0 values represent interior spaces
while updates > 0:
    updates = 0
    for x in range(maxLoc[0]):
        atEdgeX = (x == 0) or (x == maxLoc[0]-1)
        for y in range(maxLoc[1]):
            atEdgeY = (y == 0) or (y == maxLoc[1]-1)
            for z in range(maxLoc[2]):
                atEdgeZ = (y == 0) or (z == maxLoc[2]-1)
                if (cubeLocations[(x, y, z)] == 0) and \
                    ((atEdgeX or atEdgeY or atEdgeZ) or
                        (x > 0 and cubeLocations[(x-1, y, z)] == 2) or
                        (y > 0 and cubeLocations[(x, y-1, z)] == 2) or
                        (z > 0 and cubeLocations[(x, y, z-1)] == 2) or
                        (x < maxLoc[0]-1 and cubeLocations[(x+1, y, z)] == 2) or
                        (y < maxLoc[1]-1 and cubeLocations[(x, y+1, z)] == 2) or
                        (z < maxLoc[2]-1 and cubeLocations[(x, y, z+1)] == 2)):
                    cubeLocations[(x, y, z)] = 2
                    updates += 1

# Finally, search for all interior 0 values and REMOVE any face that is still
# in our exterior face set, which will leave the actual exterior faces
for x in range(maxLoc[0]):
    for y in range(maxLoc[1]):
        for z in range(maxLoc[2]):
            if cubeLocations[(x, y, z)] == 0:
                for face in Cube((x, y, z)).faceList:
                    if face in exteriorFaces:
                        exteriorFaces.remove(face)

print(f"part 2: {len(exteriorFaces)}")
