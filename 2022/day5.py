

with open('2022/day5.txt') as reader:
    allText = list(a.replace('\n', '') for a in reader.readlines())


def exec(popInOrder: bool):
    stackRowsText = list(a for a in allText if '[' in a)
    stackCount = max(line.count('[') for line in stackRowsText)
    stackList = list(list(row[i*4+1] for row in stackRowsText
                          if row[i*4+1] != ' ') for i in range(stackCount))

    movesList = list(a.split(' ') for a in allText if 'move' in a)
    movesList = list((int(a[1]), int(a[3])-1, int(a[5])-1) for a in movesList)

    for moveCount, moveFrom, moveTo in movesList:
        moveList = stackList[moveFrom][:moveCount] if popInOrder \
            else stackList[moveFrom][:moveCount][::-1]
        stackList[moveTo] = moveList + stackList[moveTo]
        stackList[moveFrom] = stackList[moveFrom][moveCount:]

    return ''.join(a[0] for a in stackList)


print(f"part 1: {exec(False)}")
print(f"part 2: {exec(True)}")
