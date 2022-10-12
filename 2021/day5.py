
import numpy as np


with open('2021/day5.txt') as reader:
    allLines = list()
    maxX, maxY = 0, 0
    for line in reader.readlines():
        line = line.strip()
        pairList = line.split(' -> ')
        x1, y1 = list(int(a) for a in pairList[0].split(','))
        x2, y2 = list(int(a) for a in pairList[1].split(','))
        maxX = max(maxX, x1, x2)
        maxY = max(maxY, y1, y2)
        allLines.append([(x1, y1), (x2, y2)])

    grid = np.zeros((maxX+1, maxY+1))
    for line in allLines:
        (x1, y1), (x2, y2) = line
        if x1 == x2:
            if y2 < y1:
                y1, y2 = y2, y1
            grid[x1, y1:y2+1] += 1
        elif y1 == y2:
            if x2 < x1:
                x1, x2 = x2, x1
            grid[x1:x2+1, y1] += 1

    result = sum(sum(grid > 1))
    print(f"part 1: result={result}")

    for line in allLines:
        (x1, y1), (x2, y2) = line
        dx, dy = (x2 - x1), (y2 - y1)
        if abs(dx) == abs(dy):
            xinc = (1 if dx > 0 else -1)
            yinc = (1 if dy > 0 else -1)
            for i in range(abs(dx)+1):
                grid[x1+i*xinc, y1+i*yinc] += 1

    result = sum(sum(grid > 1))
    print(f"part 2: result={result}")
