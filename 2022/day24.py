from queue import PriorityQueue

"""
A great article on graph search algorithms

http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
"""


class Cell:

    def __init__(self, startChar: str) -> None:
        self.startChar = startChar
        self.isWall = startChar == '#'
        self.colHarmonics = list()
        self.rowHarmonics = list()

    def __repr__(self) -> str:
        return f"[Cell start='{self.startChar}]"

    def getBlizzardCount(self, colHarmonic: int, rowHarmonic: int) -> bool:
        return (self.colHarmonics.count(colHarmonic) +
                self.rowHarmonics.count(rowHarmonic))

    def isOpen(self, colHarmonic: int, rowHarmonic: int) -> bool:
        if self.isWall:
            return False
        return self.getBlizzardCount(colHarmonic, rowHarmonic) == 0

    def getDumpChar(self, colHarmonic: int, rowHarmonic: int) -> str:
        blizzardCount = self.getBlizzardCount(colHarmonic, rowHarmonic)
        if self.isWall:
            return '#'
        if blizzardCount == 0:
            return '.'
        return chr(ord('0') + blizzardCount)


class Board:

    CELL_CHAR_DIR_VECTOR_MAP = \
        {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

    def __init__(self):

        self.cellRowList = list()
        self.moveOptions = \
            list(Board.CELL_CHAR_DIR_VECTOR_MAP.values()) + [(0, 0)]

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

    def getNeighbors(self, loc: tuple, minute):
        harmonics = list(minute % a for a in self.shape)
        neighbors = list()
        for checkVector in self.moveOptions:
            x, y = tuple(a + b for (a, b) in zip(loc, checkVector))
            if x < 0 or y < 0:
                continue
            cell = self.cellRowList[y][x]
            if cell.isOpen(*harmonics):
                neighbors.append((x, y))

        return neighbors

    def getDistance(self, loc: tuple, dest: tuple):
        return abs(dest[0] - loc[0]) + abs(dest[1] - loc[1])

    def getTimeSnapshot(self, minute: int):
        harmonics = list(minute % a for a in self.shape)
        return list(list(a.getDumpChar(*harmonics) for a in row)
                    for row in self.cellRowList)

    def dump(self, minute: int):
        snapshot = self.getTimeSnapshot(minute)
        for y, row in enumerate(snapshot):
            print(f"{''.join(a for a in row)} [{y}]")

    def findBestPathAStar(self):
        frontier = PriorityQueue()
        frontier.put((0, self.start, 1))
        cameFrom: dict[tuple, tuple] = {self.start: None}
        costSoFar: dict[tuple, float] = {self.start: 0}

        while not frontier.empty():
            _, current, minute = frontier.get()
            if current == self.destination:
                return cameFrom, costSoFar

            # What happens here if you need to STAY in the same place
            # beacuse you can't go anywhere else?
            neighbors = self.getNeighbors(current, minute)
            for next in neighbors:
                cost = costSoFar[current] + 1
                if next not in costSoFar or cost < costSoFar[next]:
                    costSoFar[next] = cost
                    priority = cost + self.getDistance(next, self.destination)
                    frontier.put((priority, next, minute+1))
                    cameFrom[next] = current

        raise RuntimeError('Never found the end')

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
result = board.findBestPathAStar()
print(f"part 1: {result}")
result = board.findBestPath(board.start, list(), 100, 0)
print(f"part 1: {result}")
