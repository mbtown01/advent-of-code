

class BingoCard:

    def __init__(self, rowData: list):
        rowCount = len(rowData[0])
        colData = list()
        diag1, diag2 = list(), list()
        for i in range(rowCount):
            colData.append(list(a[i] for a in rowData))
            diag1.append(rowData[i][i])
            diag2.append(rowData[i][rowCount-i-1])
        self._allSeries = rowData + colData + [diag1] + [diag2]
        self._hasWon = False

    def getScore(self, number: int):
        rowSums = list(sum(a) for a in self._allSeries[:5])
        overallSum = sum(rowSums)
        return overallSum * number

    def hasWon(self):
        return self._hasWon

    def checkNumber(self, number: int):
        if not self._hasWon:
            for series in self._allSeries:
                if number in series:
                    series.remove(number)
            self._hasWon = any(list(0 == len(a) for a in self._allSeries))
        return self._hasWon


with open('day4.txt') as reader:
    allNumbers = list(int(a) for a in reader.readline().split(','))
    allCardData = list()
    for line in reader.readlines():
        line = line.strip().replace('  ', ' ')
        if len(line) > 0:
            allCardData.append(list(int(a) for a in line.split(' ')))

    allCardsList = list(BingoCard(allCardData[i:i+5])
                        for i in range(0, len(allCardData), 5))

    allWinners = list()
    for number in allNumbers:
        for card in allCardsList:
            if not card.hasWon() and card.checkNumber(number):
                score = card.getScore(number)
                allWinners.append((score, number, card))
                print(f'part 1: score={score}')

    assert(len(allWinners) > 0)
    print(f"part 2: score={allWinners[-1][0]}")
