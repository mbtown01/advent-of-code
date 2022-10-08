
class Position:

    def __init__(self, state: str, x: int, y: int):
        self.state = state
        self.x = x
        self.y = y

        self.posNorth = None
        self.posSouth = None
        self.posEast = None
        self.postWest = None

    def __repr__(self) -> str:
        return f"[Position ({self.x}, {self.y}) = {self.state}]"

    def canPropEast(self):
        return ('>', '.') == (self.state, self.posEast.state)

    def propEast(self):
        self.posEast.state, self.state = (self.state, '.')

    def canPropSouth(self):
        return ('v', '.') == (self.state, self.posSouth.state)

    def propSouth(self):
        self.posSouth.state, self.state = (self.state, '.')


def dumpBoard(board: list):
    for row in board:
        print(''.join(list(a.state for a in row)))


with open('day25.txt') as reader:
    board = list()
    for y, line in enumerate(reader.readlines()):
        row = list(Position(a, x, y) for x, a in enumerate(line.strip()))
        lineLen = len(row)
        board.append(row)

    boardLen = len(board)
    for y, row in enumerate(board):
        for x, a in enumerate(row):
            a.posNorth = board[(y-1+boardLen) % boardLen][x]
            a.posSouth = board[(y+1) % boardLen][x]
            a.posEast = row[(x+1) % lineLen]
            a.postWest = row[(x-1+lineLen) % lineLen]

    stepCount, stillPropagating = 0, True
    while(stillPropagating):
        allEastBound = list(
            a for row in board for a in row if a.canPropEast())
        for a in allEastBound:
            a.propEast()
        stillPropagating = len(allEastBound) > 0

        allSouthBound = list(
            a for row in board for a in row if a.canPropSouth())
        for a in allSouthBound:
            a.propSouth()
        stillPropagating = stillPropagating or len(allSouthBound) > 0

        stepCount += 1
        # dumpBoard(board)

    # dumpBoard(board)
    print(f'done in {stepCount} steps')
