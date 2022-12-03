from typing import Callable


class Game:
    SHAPE_ROCK, SHAPE_PAPER, SHAPE_SCISSORS = 0, 1, 2
    RESULT_WIN, RESULT_DRAW, RESULT_LOSE = 6, 3, 0

    def __init__(self):
        self.playerShapeMap = dict(
            A=Game.SHAPE_ROCK, B=Game.SHAPE_PAPER, C=Game.SHAPE_SCISSORS,
            X=Game.SHAPE_ROCK, Y=Game.SHAPE_PAPER, Z=Game.SHAPE_SCISSORS)
        self.resultShapeMap = \
            dict(X=Game.RESULT_LOSE, Y=Game.RESULT_DRAW, Z=Game.RESULT_WIN)

        # Builds a map of what theirShape is to a mapping of desired outcomes
        # to what shape to play in response for easy lookup in part 2
        shapes = (Game.SHAPE_ROCK, Game.SHAPE_PAPER, Game.SHAPE_SCISSORS)
        self.mustPlayShapeMap = \
            {theirShape: {self._playResult(theirShape, myShape)[1]: myShape
                          for myShape in shapes} for theirShape in shapes}

    def _playResult(self, theirShape: int, myShape: int):
        if theirShape == myShape:
            return (Game.RESULT_DRAW, Game.RESULT_DRAW)
        if (theirShape+1) % 3 == myShape:
            return (Game.RESULT_LOSE, Game.RESULT_WIN)
        return (Game.RESULT_WIN, Game.RESULT_LOSE)

    def _playRound(self, myShapeSelector: Callable, plays: list):
        theirShape = self.playerShapeMap[plays[0]]
        myShape = myShapeSelector(plays)
        return 1 + myShape + self._playResult(theirShape, myShape)[1]

    def _selectorPart1(self, plays: list):
        return self.playerShapeMap[plays[1]]

    def _selectorPart2(self, plays: list):
        desiredResult = self.resultShapeMap[plays[1]]
        theirShape = self.playerShapeMap[plays[0]]
        return self.mustPlayShapeMap[theirShape][desiredResult]

    def part1(self, allPlays: list):
        return sum(self._playRound(self._selectorPart1, a) for a in allPlays)

    def part2(self, allPlays: list):
        return sum(self._playRound(self._selectorPart2, a) for a in allPlays)


with open('2022/day2.txt') as reader:
    allPlays = list(a.strip().split(' ') for a in reader.readlines())

print(f"part 1: {Game().part1(allPlays)}")
print(f"part 2: {Game().part2(allPlays)}")
