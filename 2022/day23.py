from collections import defaultdict


class Board:

    def __init__(self):
        self.elfMap = dict()
        self.checkVectors = [
            ((0, -1), [(-1, -1), (0, -1), (1, -1)]),    # North
            ((0, 1), [(-1, 1), (0, 1), (1, 1)]),        # South
            ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),    # West
            ((1, 0), [(1, -1), (1, 0), (1, 1)]),        # East
        ]

        with open('2022/day23.txt') as reader:
            for y, row in enumerate(reader.readlines()):
                for x, cell in enumerate(row):
                    if '#' == cell:
                        self.elfMap[(x, y)] = 1

    def playRound(self):
        # First half - identify all the moving elves and where they are
        # proposing to move
        proposedMovedMap = defaultdict(int)
        proposedMoves = list()
        for currentLoc in self.elfMap.keys():
            possibleDestinations = list()
            # Technically this could be improved.... I'm going to for sure
            # check 12 hash locations for every elf, but there are only
            # 8 unique neighbors to check.  This is so clean though, I hate
            # to make it uglier!!
            for destOffset, destCheckOffsets in self.checkVectors:
                destLocations = list((currentLoc[0] + a[0],
                                      currentLoc[1] + a[1])
                                     for a in destCheckOffsets)
                if all(a not in self.elfMap for a in destLocations):
                    proposedMove = (currentLoc[0] + destOffset[0],
                                    currentLoc[1] + destOffset[1])
                    possibleDestinations.append(proposedMove)
            if len(possibleDestinations) in [1, 2, 3]:
                proposedMove = possibleDestinations[0]
                proposedMovedMap[proposedMove] += 1
                proposedMoves.append((currentLoc, proposedMove))

        # Second half - let every elf move to their proposed location ONLY
        # if that elf is the ONLY elf proposing that location, otherwise
        # the elf does not move
        moveCount = 0
        for currentLoc, proposedMove in proposedMoves:
            if proposedMovedMap[proposedMove] == 1:
                del self.elfMap[currentLoc]
                self.elfMap[proposedMove] = 1
                moveCount += 1

        # Rotate te checkVector
        self.checkVectors = self.checkVectors[1:] + [self.checkVectors[0]]

        return moveCount

    def getDimensions(self):
        minX, minY, maxX, maxY = 999, 999, -999, -999
        for loc in self.elfMap.keys():
            minX, minY = min(minX, loc[0]), min(minY, loc[1])
            maxX, maxY = max(maxX, loc[0]), max(maxY, loc[1])
        return minX, minY, maxX, maxY

    def getEmptyCount(self):
        minX, minY, maxX, maxY = self.getDimensions()
        return (maxX - minX + 1) * (maxY - minY + 1) - len(self.elfMap)

    def dump(self):
        minX, minY, maxX, maxY = self.getDimensions()
        for y in range(minY, maxY+1):
            print(''.join(list('#' if (x, y) in self.elfMap else '.'
                               for x in range(minX, maxX+1))))


board = Board()
totalRounds = 0

for i in range(10):
    board.playRound()
    totalRounds += 1
print(f"part1: {board.getEmptyCount()}")

while board.playRound() > 0:
    totalRounds += 1

print(f"part2: {totalRounds+1}")
