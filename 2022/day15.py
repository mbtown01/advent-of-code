

def areOverlappedOrAdjacent(r1l: int, r1r: int, r2l: int, r2r: int):
    return ((r1r >= r2l and r1r <= r2r) or
            (r1l >= r2l and r1l <= r2r) or
            (r1l >= r2l and r1r <= r2r) or
            (r1l <= r2l and r1r >= r2r) or
            (r1r == r2l - 1))


def checkRow(sensorList: list, rowNum: int):
    allSpans, rowBeacons = list(), set()
    for sx, sy, bx, by in sensorList:
        manDist = abs(bx-sx) + abs(by-sy)
        rowDist = abs(sy - rowNum)
        if rowDist <= manDist:
            halfWidth = manDist - rowDist
            allSpans.append((sx-halfWidth, sx+halfWidth))
        if by == rowNum:
            rowBeacons.add(bx)

    allSpans = sorted(allSpans)
    unionedSpans, currentSpan = list(), allSpans[0]
    for thisSpan in allSpans[1:]:
        if areOverlappedOrAdjacent(*currentSpan, *thisSpan):
            currentSpan = (currentSpan[0], max(currentSpan[1], thisSpan[1]))
        else:
            unionedSpans.append(currentSpan)
            currentSpan = thisSpan
    unionedSpans.append(currentSpan)
    gap = unionedSpans[0][1]+1 if len(unionedSpans) > 1 else None
    return sum(a[1]-a[0]+1 for a in unionedSpans) - len(rowBeacons), gap


sensorList = list()
with open('2022/day15.txt') as reader:
    for line in reader.readlines():
        parts = line.strip().replace(',', '').replace(':', '').split(' ')
        coords = list(int(parts[a].split('=')[1]) for a in [2, 3, 8, 9])
        sensorList.append(coords)

print(f"part 1: {checkRow(sensorList, 2000000)[0]}")
for i in range(4000000):
    count, gap = checkRow(sensorList, i)
    if gap is not None:
        print(f"part 2: {4000000*gap+i}")
