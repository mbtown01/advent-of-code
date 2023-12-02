

class Cell:

    def __init__(self, startChar: str) -> None:
        self.startChar = startChar
        self.isWall = startChar == '#'
        self.colHarmonics = list()
        self.rowHarmonics = list()

    def __repr__(self) -> str:
        return f"[Cell start='{self.startChar}]"

    def getDumpChar(self, colHarmonic: int, rowHarmonic: int) -> str:
        blizzardCount = self.colHarmonics.count(colHarmonic) + \
            self.rowHarmonics.count(rowHarmonic)
        if self.isWall:
            return '#'
        if blizzardCount == 0:
            return '.'
        return chr(ord('0') + blizzardCount)


class Board:

    def __init__(self):
        cellCharDirVectorMap = \
            {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

        self.cellRowList = list()
        self.moveOptions = list(cellCharDirVectorMap.values()) + [(0, 0)]

        with open('2022/day24.txt') as reader:
            for row in reader.readlines():
                self.cellRowList.append(list())
                for cellChar in row.strip():
                    cell = Cell(cellChar)
                    self.cellRowList[-1].append(cell)

        self.shape = (len(self.cellRowList[0]), len(self.cellRowList))
        self.start = tuple((
            list(a.isWall for a in self.cellRowList[0]).index(False), 0))
        self.destination = tuple((
            list(a.isWall for a in self.cellRowList[-1]).index(False),
            len(self.cellRowList)-1))

        for y in range(1, self.shape[1]-1):
            cells = self.cellRowList[y][1:-1]
            charList = list(a.startChar for a in cells)
            cellCount = len(charList)
            indices = list(i for (i, a) in enumerate(charList) if a == '>')
            for i, cell in enumerate(cells):
                cell.rowHarmonics += list((i-a) % cellCount for a in indices)
            indices = list(i for (i, a) in enumerate(charList) if a == '<')
            for i, cell in enumerate(cells):
                cell.rowHarmonics += list((a-i) % cellCount for a in indices)

        for x in range(1, self.shape[0]-1):
            cells = list(a[x] for a in self.cellRowList[1:-1])
            charList = list(a.startChar for a in cells)
            cellCount = len(charList)
            indices = list(i for (i, a) in enumerate(charList) if a == 'v')
            for i, cell in enumerate(cells):
                cell.colHarmonics += list((i-a) % cellCount for a in indices)
            indices = list(i for (i, a) in enumerate(charList) if a == '^')
            for i, cell in enumerate(cells):
                cell.colHarmonics += list((a-i) % cellCount for a in indices)

        self.harmonic = self.shape[0] * self.shape[1]
        self.snapshotCache = dict()
        print('Caching...')
        for minute in range(self.harmonic):
            self.snapshotCache[minute] = self.getTimeSnapshot(minute)
        print('Cached and ready')

    def getTimeSnapshot(self, minute: int):
        harmonics = list(minute % a for a in self.shape)
        return list(list(a.getDumpChar(*harmonics) for a in row)
                    for row in self.cellRowList)

    def dump(self, minute: int):
        snapshot = self.getTimeSnapshot(minute)
        for y, row in enumerate(snapshot):
            print(f"{''.join(a for a in row)} [{y}]")

    def findBestPath(self, loc: tuple, path: list, best: int, minute: int):
        if minute >= best:
            return best
        if loc == self.destination:
            print(f"new best={minute}")
            return minute

        # You COULD figure out how long you can stay in one spot, but looking
        # at the big data, there aren't a whole lot of '.' locations...

        snapshot = self.snapshotCache[(minute + 1) % self.harmonic]
        for checkVector in self.moveOptions:
            checkLoc = tuple(a + b for (a, b) in zip(loc, checkVector))
            if any(a < 0 for a in checkLoc):
                continue
            if '.' == snapshot[checkLoc[1]][checkLoc[0]]:
                result = self.findBestPath(
                    checkLoc, path + [(minute+1, checkLoc)], best, minute+1)
                best = min(best, result)

        return best


board = Board()
result = board.findBestPath(board.start, list(), 100, 0)
print(f"part 1: {result}")
