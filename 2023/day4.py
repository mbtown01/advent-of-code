
with open('2023/day4.txt', encoding="utf8") as reader:
    cardMatchCountList = []
    for line in reader:
        winText, myText = line.strip().split(': ')[1].split(' | ')
        winNumbers = list(int(a) for a in winText.split(' ') if a != '')
        myNumbers = list(int(a) for a in myText.split(' ') if a != '')
        cardMatchCountList.append(
            sum(1 if a in winNumbers else 0 for a in myNumbers))

    cardMatchInfoMap = {i: dict(count=a, finalCount=None, matchCount=a)
                        for (i, a) in enumerate(cardMatchCountList)}

    def getCardMatchCount(index: int):
        cardMatchInfo = cardMatchInfoMap[index]
        finalCount = cardMatchInfo.get('finalCount')
        if finalCount is not None:
            return finalCount

        matchCount = cardMatchInfo['matchCount']
        cardMatchInfo['finalCount'] = 1 + sum(
            getCardMatchCount(index+1+a) for a in range(matchCount))
        return cardMatchInfo['finalCount']

    part1Sum = sum(2**(a-1) if a > 0 else 0 for a in cardMatchCountList)
    part2Sum = sum(getCardMatchCount(i) for i in range(len(cardMatchInfoMap)))

    print(f"part 1: {part1Sum}")
    print(f"part 2: {part2Sum}")
