
import unittest


class Implementation:
    part1Max = {'red': 12, 'green': 13, 'blue': 14}

    def __init__(self, dataPath: str):
        self.gameCubeCountsList = list()
        with open(dataPath, encoding="utf8") as reader:
            # self.part1Sum, self.part2Sum = 0, 0
            for line in reader:
                gameText, drawText = line.strip().split(': ')
                gameId = int(gameText.split(' ')[1])

                self.gameCubeCountsList.append((gameId, [
                    {p[1]: int(p[0]) for p in list(
                        t.split(' ') for t in s.split(', '))}
                    for s in drawText.split('; ')
                ]))

    def part1(self):
        result = 0
        for gameId, gameCubeCountList in self.gameCubeCountsList:
            if all(count <= self.part1Max[color]
                   for gameCubeCount in gameCubeCountList
                   for color, count in gameCubeCount.items()):
                result += gameId
        return result

    def part2(self):
        result = 0
        for _, gameCubeCountList in self.gameCubeCountsList:
            colorCounts = {a: 0 for a in self.part1Max}
            for gameCubeCount in gameCubeCountList:
                for color, count in gameCubeCount.items():
                    colorCounts[color] = max(colorCounts[color], count)
            localProduct = 1
            for count in colorCounts.values():
                localProduct *= count
            result += localProduct

        return result


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 8)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 2879)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 2286)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 65122)
