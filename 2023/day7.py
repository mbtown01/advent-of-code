import unittest


class Implementation:

    def __init__(self, dataPath: str):
        self.cardMatchCountList = []
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                winText, myText = line.strip().split(': ')[1].split(' | ')
                winNumbers = \
                    list(int(a) for a in winText.split(' ') if a != '')
                myNumbers = list(int(a) for a in myText.split(' ') if a != '')
                self.cardMatchCountList.append(
                    sum(1 if a in winNumbers else 0 for a in myNumbers))

        self.cardMatchInfoMap = {
            i: dict(count=a, finalCount=None, matchCount=a)
            for (i, a) in enumerate(self.cardMatchCountList)
        }

    def getCardMatchCount(self, index: int):
        cardMatchInfo = self.cardMatchInfoMap[index]
        finalCount = cardMatchInfo.get('finalCount')
        if finalCount is not None:
            return finalCount

        matchCount = cardMatchInfo['matchCount']
        cardMatchInfo['finalCount'] = 1 + sum(
            self.getCardMatchCount(index+1+a) for a in range(matchCount))
        return cardMatchInfo['finalCount']

    def part1(self):
        return sum(2**(a-1) if a > 0 else 0 for a in self.cardMatchCountList)

    def part2(self):
        return sum(self.getCardMatchCount(i)
                   for i in range(len(self.cardMatchInfoMap)))


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 13)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 23673)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 30)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 12263631)
