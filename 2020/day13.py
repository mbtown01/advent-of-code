from math import lcm

with open('2020/day13.txt') as reader:
    startTime = int(reader.readline())
    busIdText = reader.readline()
    busIdRawList = busIdText.split(',')
    busIdList = list(int(a) for a in busIdRawList if a != 'x')
    busIdOffsetMap = {int(a): i for i, a in enumerate(
        busIdRawList) if a != 'x'}

currentBest = (None, None)
for busId in busIdList:
    nextTime = (startTime // busId) * busId
    nextTime = (nextTime + busId) if nextTime < startTime else nextTime
    if currentBest[0] is None or nextTime < currentBest[0]:
        currentBest = (nextTime, busId)

nextTime, busId = currentBest
print(f"part 1: {currentBest} {(nextTime-startTime)*busId}")

# Iteratively collapse the first two pairs of sequences into a new
# macro sequence until we get the actual answer
busOffsetList = list(busIdOffsetMap[a] for a in busIdList)
offsetIdList = list(zip(busOffsetList, busIdList))
off1, id1 = offsetIdList.pop(0)
while len(offsetIdList):
    off2, id2 = offsetIdList.pop(0)
    for offTest in range(off1, id1*id2, id1):
        if (offTest - off2) % id2 == 0:
            off1, id1 = offTest, id1*id2
            print(off1, id1)
            break

print(f"part 2: {id1-off1}")
