import numpy as np


class Rock:

    CELL_MAP = {'.': 0, '#': 1}

    ALL_ROCKS = [
        ['####'],
        ['.#.', '###', '.#.'],
        ['..#', '..#', '###'],
        ['#', '#', '#', '#'],
        ['##', '##']
    ]

    def __init__(self, index: int):
        self.index = index
        self.matrix = Rock.ALL_ROCKS[index]
        self.matrix = list(
            np.array([Rock.CELL_MAP[a] for a in row]) for row in self.matrix)
        self.matrix = np.array(self.matrix, dtype=np.uint8)

    @property
    def width(self):
        return self.matrix.shape[1]

    @property
    def height(self):
        return self.matrix.shape[0]


class PlayingBoard:

    START_MARGIN = 3
    CELL_MAP_EMPTY, CELL_MAP_FALLING, CELL_MAP_COMMITTED = 0, 1, 16
    CELL_MAP_WALL, CELL_MAP_FLOOR = 3, 4
    CELL_MAP = {
        CELL_MAP_EMPTY: '.', CELL_MAP_FALLING: '%',
        CELL_MAP_WALL: '|', CELL_MAP_FLOOR: '-',
        CELL_MAP_COMMITTED + 0: '1', CELL_MAP_COMMITTED + 1: '2',
        CELL_MAP_COMMITTED + 2: '3',
        CELL_MAP_COMMITTED + 3: '4',
        CELL_MAP_COMMITTED + 4: '5',
    }

    def __init__(self, width: int, maxRows: int = 20):
        self.maxRows = maxRows
        self.matrix = np.zeros((maxRows+1, width+2), dtype=np.uint8)
        self.matrix[:, 0] = PlayingBoard.CELL_MAP_WALL
        self.matrix[:, -1] = PlayingBoard.CELL_MAP_WALL
        self.matrix[-1, :] = PlayingBoard.CELL_MAP_FLOOR
        self.lastRow = 0
        self.highestRow = 0

    def startRock(self, rock: Rock):
        x, y = 2+1, self.highestRow + 4 + rock.height - 1
        return x, y

    def _rowIndexToGlobalY(self, index: int):
        return self.maxRows + self.lastRow - index

    def _globalYToRowIndex(self, y: int):
        return self.maxRows - (y - self.lastRow)

    def canPlaceRock(self, rock: Rock, x: int, y: int):
        localY = self._rowIndexToGlobalY(y)
        rockUnion = (self.matrix[localY:localY+rock.height, x:x+rock.width] +
                     rock.matrix) * rock.matrix
        return rockUnion.max() == PlayingBoard.CELL_MAP_FALLING

    def commitRock(self, rock: Rock, x: int, y: int):
        localY = self._rowIndexToGlobalY(y)
        self.matrix[localY:localY+rock.height, x:x+rock.width] += \
            rock.matrix * (PlayingBoard.CELL_MAP_COMMITTED + rock.index)
        self.highestRow = max(y, self.highestRow)

    def dump(self, rock: Rock = None, x: int = None, y: int = None,
             rowCount: int = None):
        matrix = self.matrix.copy()
        if rock is not None:
            localY = self._rowIndexToGlobalY(y)
            matrix[localY:localY+rock.height, x:x+rock.width] += rock.matrix
        topRow = self._globalYToRowIndex(self.highestRow)
        lastRow = topRow+rowCount if rowCount is not None else -1
        for i, row in enumerate(matrix[topRow:lastRow]):
            rowText = \
                ''.join(PlayingBoard.CELL_MAP.get(a, '!') for a in row)
            print(f"{rowText} [{self._globalYToRowIndex(i+topRow)}]")
        print(self.highestRow)


def dropBlocks(wind: list, count: int, maxRows: int = 1000000,
               oneCycle: bool = False):
    rocks = list(Rock(a) for a in range(len(Rock.ALL_ROCKS)))
    t, board = 0, PlayingBoard(7, maxRows=maxRows)
    cycleHeightMap, cycleList = dict(), list()
    for r in range(0, count):
        prevHighestRow, prevT = board.highestRow, t % len(wind)
        rock = rocks[r % len(Rock.ALL_ROCKS)]
        x, y = board.startRock(rock)
        if not board.canPlaceRock(rock, x, y):
            raise RuntimeError("Uh, this should never happen")
        for y in range(y, 0, -1):
            t, w = t+1, wind[t % len(wind)]
            if board.canPlaceRock(rock, x+w, y):
                x += w
            if not board.canPlaceRock(rock, x, y-1):
                break
        board.commitRock(rock, x, y)

        if oneCycle:
            topRow = board._globalYToRowIndex(board.highestRow)
            boardHash = tuple(board.matrix[topRow:topRow+16].flatten())
            cycleIndex = (r % len(Rock.ALL_ROCKS), prevT, t %
                          len(wind), boardHash)
            if cycleIndex in cycleHeightMap:
                return dict(
                    board=board,
                    rampBlocks=cycleList.index(cycleIndex),
                    rampHeight=cycleHeightMap[cycleIndex],
                    cycleBlocks=len(cycleList) - cycleList.index(cycleIndex),
                    cycleHeight=prevHighestRow - cycleHeightMap[cycleIndex])
            cycleHeightMap[cycleIndex] = prevHighestRow
            cycleList.append(cycleIndex)

    return dict(board=board)


with open('2022/day17.txt') as reader:
    wind = ''.join(a.strip() for a in reader.readlines())
    wind = list(1 if a == '>' else -1 for a in wind)

result = dropBlocks(wind, 2022)
print(f"part 1: {result['board'].highestRow}")

finalTowerHeight = 1000000000000
result = dropBlocks(wind, 100000, oneCycle=True)
cycleCount, blockRemaining = \
    divmod(finalTowerHeight - result['rampBlocks'], result['cycleBlocks'])
finalHeight = result['rampHeight'] + result['cycleHeight'] * cycleCount
if blockRemaining > 0:
    finalResult = dropBlocks(
        wind, result['rampBlocks'] + result['cycleBlocks'] + blockRemaining)
    finalHeight += finalResult['board'].highestRow - \
        result['rampHeight'] - result['cycleHeight']

print(f"part 2: {finalHeight}")
