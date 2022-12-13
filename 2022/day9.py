

def dumpGrid(rope: list, visitedMap: dict):
    ropeMap = {a: '#' for a in visitedMap.keys()}
    ropeMap.update({(a[0], a[1]): str(i) for i, a in enumerate(rope)})
    minX, minY, maxX, maxY = 0, 0, 0, 0
    for x, y in ropeMap.keys():
        minX, minY = min(minX, x), min(minY, y)
        maxX, maxY = max(maxX, x), max(maxY, y)

    for j in reversed(range(minY, maxY+1)):
        line = list(ropeMap.get((i, j), '.') for i in range(minX, maxX+1))
        print(' '.join(line))
    print()


def chaseRope(movesList: list, ropeLen: int):
    changeMap = dict(U=(0, 1), D=(0, -1), L=(-1, 0), R=(1, 0))
    deltaPosMap = {
        (x, y): tuple([x//abs(x) if x != 0 else 0, y//abs(y) if y != 0 else 0])
        for x in range(-2, 3) for y in range(-2, 3) if abs(x) == 2 or abs(y) == 2
    }

    rope = [(0, 0)] * ropeLen
    visitedMap = {rope[0]: True}
    for move, distance in movesList:
        change = changeMap[move]
        for d in range(distance):
            rope[0] = tuple(rope[0][i] + change[i] for i in range(2))
            for knotIndex in range(1, len(rope)):
                headPos, tailPos = rope[knotIndex-1], rope[knotIndex]
                deltaPos = tuple(headPos[i] - tailPos[i] for i in range(2))
                knotMove = deltaPosMap.get(deltaPos)
                if knotMove is None:
                    break
                rope[knotIndex] = tuple(
                    tailPos[a] + knotMove[a] for a in range(2))
            visitedMap[rope[-1]] = True

            # print(f"{move} {distance} ({d})")
            # dumpGrid(rope, visitedMap)
    return len(visitedMap)


with open('2022/day9.txt') as reader:
    movesList = list((a.strip().split(' ')) for a in reader.readlines())
    movesList = list((a[0], int(a[1])) for a in movesList)


print(f"part 1: {chaseRope(movesList, 2)}")
print(f"part 2: {chaseRope(movesList, 10)}")
