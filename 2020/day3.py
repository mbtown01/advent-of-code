

with open('2020/day3.txt') as reader:
    grid = list(a.strip() for a in reader.readlines())


def getTreeCount(slopeX: int, slopeY: int):
    gridWidth = len(grid[0])
    treeCount, x, y = 0, slopeX, slopeY
    while y < len(grid):
        if grid[y][x] == '#':
            treeCount += 1
        x = (x+slopeX) % gridWidth
        y = y + slopeY

    return treeCount


product = 1
for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    treeCount = getTreeCount(*slope)
    print(f"slope={slope}, treeCount={treeCount}")
    product *= treeCount

print(f"product={product}")
