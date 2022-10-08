from math import sqrt, ceil
import numpy as np

# input = 'target area: x=20..30, y=-10..-5'
input = 'target area: x=128..160, y=-142..-88'

_, ranges = input.split(': ')
rangeX, rangeY = ranges.split(', ')
minX, maxX = list(int(a) for a in rangeX.replace('x=', '').split('..'))
minY, maxY = list(int(a) for a in rangeY.replace('y=', '').split('..'))

xPathCache = dict()
yPathCache = dict()


def findAllPaths(endX: int, endY: int):
    """ Start is 0, 0
    maximum x velocity:
        velocity's first step can't be past maxX
        vx = endX
    minimum x velocity:
        velocity has to terminate at or past minX
        endX = (vx^2 + vx)/2
        vx^2 + vx - 2*endX = 0
    minimum y velocity
        vy = endY
    maximum y velocity:
        vy = -endY -1
    """

    xList = xPathCache.get(endX)
    if xList is None:
        bigTerm = sqrt(1+4*(2*endX))/2
        minX, maxX = int(ceil(max(-1 + bigTerm, -1 - bigTerm))), endX
        xList = list()
        for vx in range(minX, maxX+1):
            xSet = set(np.cumsum(range(vx, 0, -1)))
            if endX in xSet:
                xList.append(vx)
        xPathCache[endX] = xList

    yList = yPathCache.get(endY)
    if yList is None:
        yList = list()
        minY, maxY = endY, -endY-1
        for vy in range(minY, maxY+1):
            thisVy, y = vy, 0
            while y > endY:
                y, thisVy = y + thisVy, thisVy-1
                if y == endY:
                    yList.append(vy)
        yPathCache[endY] = yList

    points = set()
    for vx in xList:
        for vy in yList:
            x, y, thisVx, thisVy = 0, 0, vx, vy
            while y > endY and x <= endX:
                x, y = x+thisVx, y+thisVy
                thisVx, thisVy = max(0, thisVx-1), thisVy-1
                if y == endY and x == endX:
                    points.add((vx, vy))

    return points


def part1(minY: int):
    vy = abs(minY)-1
    heightMax = vy*(vy+1)/2
    return heightMax


allPoints = set()
for x in range(minX, maxX + 1):
    for y in range(minY, maxY+1):
        for value in findAllPaths(x, y):
            allPoints.add(value)


part1(minY)


print(f'part 2: {len(allPoints)}')
