from collections import defaultdict

fieldValueSetMap = defaultdict(set)
allFieldsSet = set()

with open('2020/day16.txt', encoding='utf8') as reader:
    allLines = list(a.strip() for a in reader.readlines())

while allLines[0] != '':
    field, ranges = allLines[0].split(': ')
    r1, r2 = ranges.split(' or ')
    for rangePair in r1, r2:
        v1, v2 = rangePair.split('-')
        for fieldValue in range(int(v1), int(v2)+1):
            fieldValueSetMap[fieldValue].add(field)
    allFieldsSet.add(field)
    allLines = allLines[1:]

myTicket = allLines[2].split(',')
allLines = allLines[5:]

errorRate = 0
validTickets = list()
while len(allLines) > 0:
    nearbyValues = list(int(a) for a in allLines[0].split(','))
    errorCount = 0
    for value in nearbyValues:
        if value not in fieldValueSetMap:
            errorCount += value
    if errorCount == 0:
        validTickets.append(nearbyValues)
    errorRate += errorCount
    allLines = allLines[1:]

print(f"Error rate: {errorRate}")

fieldSetList = list(set(allFieldsSet) for _ in validTickets[0])
for ticket in validTickets:
    for i, fieldValue in enumerate(ticket):
        fieldSet = fieldValueSetMap[fieldValue]
        fieldSetList[i] = fieldSetList[i].intersection(fieldSet)

while True:
    solvedFieldList = list(list(a)[0] for a in fieldSetList if len(a) == 1)
    if len(solvedFieldList) == len(fieldSetList):
        break
    for i, fieldSet in enumerate(fieldSetList):
        if len(fieldSetList[i]) > 1:
            fieldSetList[i] = fieldSetList[i].difference(solvedFieldList)

print(f"foo {1}")
