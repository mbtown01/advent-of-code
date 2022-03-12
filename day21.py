from functools import reduce
from collections import defaultdict


UNIVERSE_SPLITS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


class DeterministicDie:

    def __init__(self) -> None:
        self.rolls = 0

    def rollThree(self):
        total = 0
        for _ in range(3):
            total += (self.rolls % 100) + 1
            self.rolls += 1
        return total


class Player:

    def __init__(self, id: int, position: int) -> None:
        self.id = id
        self.initialPosition = self.position = position-1
        self.score = 0

    def reset(self):
        self.position = self.initialPosition
        self.score = 0

    def __repr__(self) -> str:
        return f"[Player {self.id}]"

    def takeTurn(self, die: DeterministicDie):
        moveCount = die.rollThree()
        self.position = (self.position + moveCount) % 10
        self.score += self.position + 1


def playGame(winningScore: int,
             die: DeterministicDie,
             player1: Player,
             player2: Player):
    thisPlayer, nextPlayer = player1, player2
    while(True):
        for _ in range(2):
            thisPlayer.takeTurn(die)
            if thisPlayer.score >= winningScore:
                return thisPlayer, nextPlayer
            thisPlayer, nextPlayer = nextPlayer, thisPlayer


class StartingSpace:

    def __init__(self, value: int) -> None:
        self.value = value
        self.movesMap = dict()
        self.winningPathsByTurn = defaultdict(list)

    def __repr__(self) -> str:
        return f"[StartingSpace {self.value+1}]"

    def getWinsForTurn(self, turn: int):
        wins, pathList = 0, self.winningPathsByTurn.get(turn, [])
        for path in pathList:
            wins += reduce(
                lambda a, b: a*b, (UNIVERSE_SPLITS[a] for a in path))
        return wins

    def findAllWinningPaths(self, start, score, path):
        if score >= 21:
            start.winningPathsByTurn[len(path)].append(path)
        else:
            for roll, startingSpace in self.movesMap.items():
                startingSpace.findAllWinningPaths(
                    start, score + startingSpace.value+1, path + [roll])


playerList = [Player(1, 8), Player(2, 2)]

die = DeterministicDie()
winner, loser = playGame(1000, die, *playerList)
print(f"part 1: {loser.score*die.rolls}")

for player in playerList:
    player.reset()


startingSpaceList = list(StartingSpace(a) for a in range(10))
for startingSpace in startingSpaceList:
    for roll in [3, 4, 5, 6, 7, 8, 9]:
        nextSpace = (startingSpace.value + roll) % 10
        startingSpace.movesMap[roll] = startingSpaceList[nextSpace]

competingSpaceList = list(
    startingSpaceList[a.initialPosition] for a in playerList)

for startingSpace in competingSpaceList:
    startingSpace.findAllWinningPaths(startingSpace, 0, list())

allTurnsWithWins = set(
    competingSpaceList[0].winningPathsByTurn.keys()).union(
    competingSpaceList[1].winningPathsByTurn.keys()
)

totalWins = [0, 0]
univMine, univTheirs = 1, 1
for turn in range(1, max(allTurnsWithWins)+1):
    for player, competingSpace in enumerate(competingSpaceList):
        winsForTurn = competingSpace.getWinsForTurn(turn)
        wins = winsForTurn*univMine
        totalWins[player] += wins
        univTheirs = 27*univTheirs - winsForTurn
        univTheirs, univMine = univMine, univTheirs

print(f"part 2: {totalWins}")


# Using the same starting positions as in the example above, player 1 wins in
# 444356092776315 universes, while player 2 merely wins in 341960390180808
# universes.
