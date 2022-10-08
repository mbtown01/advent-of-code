

from functools import reduce

with open('day9.txt') as reader:

    allRows = list()
    for line in reader.readlines():
        allRows.append(list(int(a) for a in line.strip()))

    lowPoints = list()
    for j, row in enumerate(allRows):
        noCheckUp, noCheckDown = j == 0, j == (len(allRows)-1)
        for i, height in enumerate(row):
            noCheckLeft, noCheckRight = i == 0, i == (len(row)-1)
            if ((noCheckLeft or height < row[i-1]) and
                    (noCheckRight or height < row[i+1]) and
                    (noCheckUp or height < allRows[j-1][i]) and
                    (noCheckDown or height < allRows[j+1][i])):
                lowPoints.append((i, j, height))

    riskLevel = sum(c+1 for a, b, c in lowPoints)
    print(f"part 1: riskLevel={riskLevel}")

    def getBasinSize(i, j):
        count, row, height = 0, allRows[j], allRows[j][i]
        if height < 9:
            noCheckUp, noCheckDown = j == 0, j == (len(allRows)-1)
            noCheckLeft, noCheckRight = i == 0, i == (len(row)-1)
            row[i], count = 9, 1
            if not noCheckLeft:
                count += getBasinSize(i-1, j)
            if not noCheckRight:
                count += getBasinSize(i+1, j)
            if not noCheckUp:
                count += getBasinSize(i, j-1)
            if not noCheckDown:
                count += getBasinSize(i, j+1)

        return count

    basinSizes = list()
    for i, j, height in lowPoints:
        size = getBasinSize(i, j)
        basinSizes.append((i, j, size))

    basinSizes.sort(key=lambda a: -a[2])
    finalSizes = list(a[2] for a in basinSizes[:3])
    answer = reduce(lambda a, b: a*b, finalSizes)
    print(f"part 2: answer={answer}")

    exit(0)
