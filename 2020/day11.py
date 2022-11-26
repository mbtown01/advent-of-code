
from cv2 import threshold


with open('2020/day11.txt') as reader:
    allRows = list(a.strip() for a in reader.readlines())

neighborsXY = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1)
]


def getNeighborsPart1(x: int, y: int, currentRows: list):
    return list(
        currentRows[y+relY][x+relX]
        for relX, relY in neighborsXY
        if y+relY >= 0 and y+relY < len(currentRows) and
        x+relX >= 0 and x+relX < len(currentRows[0])
    )


def getNeighborsPart2(x: int, y: int, currentRows: list):
    neighbors = list()
    for relX, relY in neighborsXY:
        # Walk in the relative direction until the end OR until we hit
        # a non '.'
        curX, curY = x+relX, y+relY
        while curY >= 0 and curY < len(currentRows) and \
                curX >= 0 and curX < len(currentRows[0]):
            if currentRows[curY][curX] != '.':
                neighbors.append(currentRows[curY][curX])
                break
            curX, curY = curX+relX, curY+relY

    return neighbors


def getNewPosType(x: int, y: int, posType: str, currentRows: list,
                  threshold: int, getNeighbors):
    neighbors = getNeighbors(x, y, currentRows)

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    if posType == 'L' and '#' not in neighbors:
        return '#'

    # If a seat is occupied (#) and four or more seats adjacent to it are also
    # occupied, the seat becomes empty.
    occupiedNeighbors = sum(1 if a == '#' else 0 for a in neighbors)
    if posType == '#' and occupiedNeighbors >= threshold:
        return 'L'

    # Otherwise, the seat's state does not change
    return posType


def run(currentRows: list, getNeighbors, threshold: int):
    while True:
        changeCount = 0
        newAllRows = list()
        for y, row in enumerate(currentRows):
            newAllRows.append(list())
            for x, posType in enumerate(row):
                if posType != '.':
                    newPosType = getNewPosType(
                        x, y, posType, currentRows, threshold, getNeighbors)
                    if newPosType != posType:
                        changeCount += 1
                    posType = newPosType
                newAllRows[-1].append(posType)

        # print()
        # for row in newAllRows:
        #     print(''.join(row))

        currentRows = newAllRows
        print(changeCount)
        if changeCount == 0:
            return sum(1 if a == '#' else 0 for row in currentRows for a in row)


# part1 = run(allRows, getNeighborsPart1, 4)
# print(f"part 1: {part1}")

part2 = run(allRows, getNeighborsPart2, 5)
print(f"part 2: {part2}")
