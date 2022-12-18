

def dumpMatrix(matrix: list, path: list):
    for j, row in enumerate(matrix):
        output = list()
        for i, a in enumerate(row):
            char = chr(a+ord('a'))
            if (i, j) in path:
                char = chr(ord('A') + path.index((i, j)) % 26)
            if a == 100:
                char = ' '
            output.append(char)
        print(f"{''.join(output)} [{j}]")
    print()


def findDistances(matrix: list, loc: tuple, allLocSteps: dict, path: list,
                  finalValue: int, directionFactor: int, maxSteps: int):
    # NOTE that this only works going up-hill becuase there's not a big
    # patch of 'z' values.  Really this needs to seek the final (i,j) but
    # this solution works becaues for now so I'm okay...
    (i, j), maxj, maxi = loc, len(matrix)-1, len(matrix[0])-1
    prevBest = allLocSteps.get(loc)
    if prevBest is not None and len(prevBest) <= len(path) or len(path) > maxSteps:
        return
    allLocSteps[loc] = path
    if finalValue is not None and matrix[j][i] == finalValue:
        return

    nextStepLocs = list()
    if i > 0 and (matrix[j][i-1] - matrix[j][i]) * directionFactor <= 1:
        nextStepLocs.append((i-1, j))
    if j > 0 and (matrix[j-1][i] - matrix[j][i]) * directionFactor <= 1:
        nextStepLocs.append((i, j-1))
    if i < maxi and (matrix[j][i+1] - matrix[j][i]) * directionFactor <= 1:
        nextStepLocs.append((i+1, j))
    if j < maxj and (matrix[j+1][i] - matrix[j][i]) * directionFactor <= 1:
        nextStepLocs.append((i, j+1))

    for nextStepLoc in nextStepLocs:
        findDistances(matrix, nextStepLoc, allLocSteps, path + [loc],
                      finalValue, directionFactor, maxSteps)


with open('2022/day12.txt') as reader:
    matrix = list([ord(a) - ord('a') for a in line.strip()]
                  for line in reader.readlines())

startLoc, endLoc = None, None
start, end = ord('S') - ord('a'), ord('E') - ord('a')
for j, row in enumerate(matrix):
    if start in row:
        startLoc = (row.index(start), j)
        matrix[j][startLoc[0]] = 0
    if end in row:
        endLoc = (row.index(end), j)
        matrix[j][endLoc[0]] = 25
if None in [startLoc, endLoc]:
    raise RuntimeError('no start and/or end')

allLocSteps = dict()
findDistances(matrix, startLoc, allLocSteps, [], None, 1, 500)
dumpMatrix(matrix, allLocSteps[endLoc])
print(f"part 1: {len(allLocSteps[endLoc])}")

allLocSteps = dict()
findDistances(matrix, endLoc, allLocSteps, [], 0, -1, 500)
potentialPaths = list((dest, path) for dest, path in allLocSteps.items()
                      if matrix[dest[1]][dest[0]] == 0)
finalLoc, path = min(potentialPaths, key=lambda a: len(a[1]))
dumpMatrix(matrix, path)
print(f"part 2: {len(path)}")
