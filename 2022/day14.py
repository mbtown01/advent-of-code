import numpy as np

BOARD_VAL_MAP = {0: '.', 1: 'o', 2: '#'}


def dumpBoard(board: np.array):
    for j in range(board.shape[0]):
        print(f"{''.join(BOARD_VAL_MAP[a] for a in board[j, :])} [{j}]")


def letItRainSand(wallList: list, hasFloor: bool):
    dropLoc = (500, 0)
    maxX = max(a[0] for b in wallList for a in b)
    maxY = max(a[1] for b in wallList for a in b)
    minX = min(a[0] for b in wallList for a in b)
    minY = dropLoc[1]

    if hasFloor:
        maxY += 2
        height = maxY - minY + 1
        minX = dropLoc[0] - height
        maxX = dropLoc[0] + height
        width = maxX-minX + 1
        board = np.zeros((height, width), np.int8)
        board[maxY, :] = 2
    else:
        height = maxY - minY + 1
        width = maxX-minX + 1
        board = np.zeros((height, width), np.int8)

    for wall in wallList:
        for p1, p2 in zip(wall[:-1], wall[1:]):
            if p1[0] > p2[0] or p1[1] > p2[1]:
                p1, p2 = p2, p1
            for y in range(p1[1], p2[1]+1):
                for x in range(p1[0], p2[0]+1):
                    board[y-minY, x-minX] = 2

    totalGrains = 0
    while (True):
        stillFalling, gx, gy = True, dropLoc[0]-minX, dropLoc[1]-minY
        while (stillFalling and gy < height and gx >= 0 and gx < width):
            if board[gy+1, gx] == 0:
                gx, gy = gx, gy+1
            elif gx < 0 or board[gy+1, gx-1] == 0:
                gx, gy = gx-1, gy+1
            elif gx >= width or board[gy+1, gx+1] == 0:
                gx, gy = gx+1, gy+1
            else:
                stillFalling = False

        if stillFalling or board[gy, gx] == 1:
            dumpBoard(board)
            return totalGrains

        board[gy, gx] = 1
        totalGrains += 1


wallList = list()
with open('2022/day14.txt') as reader:
    for line in reader.readlines():
        parts = list(a.split(',') for a in line.strip().split(' -> '))
        parts = list((int(a), int(b)) for (a, b) in parts)
        wallList.append(parts)

print(f"part 1: {letItRainSand(wallList, False)}")
print(f"part 2: {letItRainSand(wallList, True)}")
