

from functools import reduce

allRows = list()
with open('day11.txt') as reader:
    for line in reader.readlines():
        allRows.append(list(int(a) for a in line.strip()))


def flash(i: int, j: int):
    jMin, jMax = max(j-1, 0), min(j+1, len(allRows)-1)
    iMin, iMax = max(i-1, 0), min(i+1, len(allRows[0])-1)

    flashCount = 1
    for ej in range(jMin, jMax+1):
        for ei in range(iMin, iMax+1):
            allRows[ej][ei] += 1
            if allRows[ej][ei] == 10:
                flashCount += flash(ei, ej)

    return flashCount


def incrementEnergy():
    flashCount = 0
    for j, row in enumerate(allRows):
        for i in range(len(row)):
            row[i] += 1
            if row[i] == 10:
                flashCount += flash(i, j)

    for j, row in enumerate(allRows):
        for i in range(len(row)):
            row[i] = 0 if row[i] >= 10 else row[i]

    return flashCount


flashCount = sum(incrementEnergy() for a in range(100))
print(f"part 1: flashCount={flashCount}")

allRows = list()
with open('day11.txt') as reader:
    for line in reader.readlines():
        allRows.append(list(int(a) for a in line.strip()))

iterations = 1
while True:
    flashCount = incrementEnergy()
    if flashCount == len(allRows)*len(allRows[0]):
        break
    iterations += 1

print(f"part 2: iterations={iterations}")
exit(0)
