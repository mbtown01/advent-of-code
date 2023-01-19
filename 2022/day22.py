from enum import Enum


class CellDirection(Enum):
    RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

    def opposite(self):
        return CellDirection((self.value+2) % len(CellDirection))


class Cell:

    def __init__(self, row: int, column: int, cellChar: str) -> None:
        self.row = row
        self.column = column
        self.cellChar = cellChar
        self.dumpChar = cellChar
        self.neighbors = dict()

    def __repr__(self) -> str:
        return f"[Cell '{self.cellChar}' row={self.row} col={self.column}]"


class Board:

    def __init__(self):
        self.cellRowList = list()
        self.allDirections = list()

        with open('2022/day22.txt') as reader:
            allLines = reader.readlines()
            allMapLines = allLines[:allLines.index('\n')]
            maxColumns = max(len(a)-1 for a in allMapLines)
            for row, line in enumerate(allMapLines):
                self.cellRowList.append([None] * maxColumns)
                for column, cellChar in enumerate(line[:-1]):
                    if cellChar != ' ':
                        self.cellRowList[-1][column] = Cell(
                            row, column, cellChar)

            allDirectionsLines = allLines[allLines.index('\n')+1:]
            allDirectionsText = ''.join(a.strip() for a in allDirectionsLines)
            lagIndex = 0
            for seekIndex in range(len(allDirectionsText)):
                if allDirectionsText[seekIndex] in ['L', 'R']:
                    count = int(allDirectionsText[lagIndex:seekIndex])
                    nextDirInc = 1 if allDirectionsText[seekIndex] == 'R' else -1
                    self.allDirections.append((count, nextDirInc))
                    lagIndex = seekIndex + 1
            if lagIndex < len(allDirectionsText):
                count = int(allDirectionsText[lagIndex:])
                self.allDirections.append((count, 0))

        dim1, dim2 = len(self.cellRowList), len(self.cellRowList[0])
        self.edgeLength = min([dim1, dim2]) // 3

        faceLocationlist = list()
        for y, row in enumerate(self.cellRowList[::self.edgeLength]):
            for x, value in enumerate(row[::self.edgeLength]):
                if value is not None:
                    faceLocationlist.append((x, y))
        self.faceLocationMap = \
            {a+1: b for (a, b) in enumerate(faceLocationlist)}

        self.setupDefaultNeighbors()

    def setupDefaultNeighbors(self):
        for row in self.cellRowList:
            cells = list(a for a in row if a is not None)
            for i, cell in enumerate(cells):
                cell.neighbors[CellDirection.RIGHT] = \
                    (cells[(i+1) % len(cells)], CellDirection.RIGHT)
                cell.neighbors[CellDirection.LEFT] = \
                    (cells[(i-1) % len(cells)], CellDirection.LEFT)
        for colIndex in range(len(self.cellRowList[0])):
            cells = list(a[colIndex] for a in self.cellRowList if a[colIndex])
            for i, cell in enumerate(cells):
                cell.neighbors[CellDirection.DOWN] = \
                    (cells[(i+1) % len(cells)], CellDirection.DOWN)
                cell.neighbors[CellDirection.UP] = \
                    (cells[(i-1) % len(cells)], CellDirection.UP)

    def executePath(self):
        currentCell = list(a for a in self.cellRowList[0] if a is not None)[0]
        currentCell.dumpChar = chr(65)
        steps, currentDir = 1, CellDirection.RIGHT
        for count, nextDirInc in self.allDirections:
            nextCell, nextDir = currentCell.neighbors[currentDir]
            while count > 0 and nextCell.cellChar != '#':
                nextCell.dumpChar = chr(65 + steps % 26)
                currentCell, currentDir = nextCell, nextDir
                nextCell, nextDir = currentCell.neighbors[currentDir]
                count, steps = count - 1, steps + 1

            currentDir = CellDirection(
                (currentDir.value + nextDirInc) % len(CellDirection))

        print(f"total steps: {steps}")
        return (1000 * (currentCell.row+1) +
                4 * (currentCell.column+1) + currentDir.value)

    def getEdgeCells(self, face: int, edge: CellDirection):
        x1, y1 = (a*self.edgeLength for a in self.faceLocationMap[face])
        x2, y2 = x1 + self.edgeLength, y1 + self.edgeLength
        if edge == CellDirection.UP:
            return self.cellRowList[y1][x1:x2]
        if edge == CellDirection.DOWN:
            return self.cellRowList[y2-1][x1:x2]
        if edge == CellDirection.LEFT:
            return list(a[x1] for a in self.cellRowList[y1:y2])
        if edge == CellDirection.RIGHT:
            return list(a[x2-1] for a in self.cellRowList[y1:y2])

    def connectNeighborsByPath(self, path: list):
        toPath = list(path[(i+1) % len(path)] for i in range(len(path)))
        for (fromFace, fromDir, step), (toFace, toDir, _) in zip(path, toPath):
            fromCells = self.getEdgeCells(fromFace, fromDir)
            toCells = self.getEdgeCells(toFace, toDir.opposite())
            for fromCell, toCell in zip(fromCells, toCells[::step]):
                fromCell.neighbors[fromDir] = (toCell, toDir)
                toCell.neighbors[toDir.opposite()] = \
                    (fromCell, fromDir.opposite())

    def sanityCheckFaceDir(self, face: int, dir: CellDirection):
        startFace, currentDir = face, dir
        x, y = (a*self.edgeLength for a in self.faceLocationMap[startFace])
        startCell = currentCell = self.cellRowList[y][x]
        for _ in range(4*self.edgeLength):
            currentCell, currentDir = currentCell.neighbors[currentDir]
        if startCell != currentCell:
            raise RuntimeError("path doesn't map back on itself")

    def dump(self):
        print()
        for row in self.cellRowList:
            cellCharList = list(
                a.dumpChar if a is not None else ' ' for a in row)
            print(''.join(cellCharList))


board = Board()
print(f"part 1: {board.executePath()}")
# board.dump()

# ....11..
# ....11..
# 223344..
# 223344..
# ....5566
# ....5566

# 6 faces, 4 edges == 24 total mapping (12 pairs)
# 3 unique circular paths around the cube
#   2R -> 3R -> 4R /> 6D /> 2R
#   2U /> 1D -> 4D -> 5D /> 2U
#   3U /> 1R /> 6L -> 5L /> 3U

# board = Board()
# board.connectNeighborsByPath([
#     (2, CellDirection.RIGHT, 1),
#     (3, CellDirection.RIGHT, 1),
#     (4, CellDirection.RIGHT, -1),
#     (6, CellDirection.DOWN, -1),
# ])
# board.connectNeighborsByPath([
#     (2, CellDirection.UP, -1),
#     (1, CellDirection.DOWN, 1),
#     (4, CellDirection.DOWN, 1),
#     (5, CellDirection.DOWN, -1),
# ])
# board.connectNeighborsByPath([
#     (3, CellDirection.UP, 1),
#     (1, CellDirection.RIGHT, -1),
#     (6, CellDirection.LEFT, 1),
#     (5, CellDirection.LEFT, -1),
# ])
# print(f"part 2: {board.executePath()}")
# board.dump()


# ..1122
# ..1122
# ..33..
# ..33..
# 4455..
# 4455..
# 66....
# 66....

board = Board()
board.connectNeighborsByPath([
    (1, CellDirection.DOWN, 1),
    (3, CellDirection.DOWN, 1),
    (5, CellDirection.DOWN, 1),
    (6, CellDirection.LEFT, 1),
])
board.connectNeighborsByPath([
    (4, CellDirection.RIGHT, 1),
    (5, CellDirection.RIGHT, -1),
    (2, CellDirection.LEFT, 1),
    (1, CellDirection.LEFT, -1),
])
board.connectNeighborsByPath([
    (4, CellDirection.DOWN, 1),
    (6, CellDirection.DOWN, 1),
    (2, CellDirection.DOWN, 1),
    (3, CellDirection.LEFT, 1),
])
board.sanityCheckFaceDir(4, CellDirection.RIGHT)
board.sanityCheckFaceDir(4, CellDirection.UP)
board.sanityCheckFaceDir(6, CellDirection.RIGHT)
# 6387 TOO LOW
# 54393 too low
print(f"part 2: {board.executePath()}")
# board.dump()
