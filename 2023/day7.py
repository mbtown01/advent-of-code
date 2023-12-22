import unittest
from enum import Enum


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Implementation:

    handTypeTransitionMap = {
        HandType.HIGH_CARD: HandType.ONE_PAIR,
        HandType.ONE_PAIR: HandType.THREE_OF_A_KIND,
        HandType.TWO_PAIRS: HandType.FULL_HOUSE,
        HandType.THREE_OF_A_KIND: HandType.FOUR_OF_A_KIND,
        HandType.FULL_HOUSE: HandType.FOUR_OF_A_KIND,
        HandType.FOUR_OF_A_KIND: HandType.FIVE_OF_A_KIND,
        HandType.FIVE_OF_A_KIND: HandType.FIVE_OF_A_KIND,
    }

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.handList = list(a.strip().split(' ') for a in reader)
            self.handList = list((a, int(b)) for a, b in self.handList)

    def classifyHandType(self, hand: str):
        cardCountMap = {a: hand.count(a) for a in hand}
        cardCountList = sorted(cardCountMap.values())

        if len(cardCountMap) > 0:
            if cardCountList[-1] == 5:
                return HandType.FIVE_OF_A_KIND
            if cardCountList[-1] == 4:
                return HandType.FOUR_OF_A_KIND
            if len(cardCountMap) > 1:
                if cardCountList[-2] == 2 and cardCountList[-1] == 3:
                    return HandType.FULL_HOUSE
                if cardCountList[-2] == 2 and cardCountList[-1] == 2:
                    return HandType.TWO_PAIRS
            if cardCountList[-1] == 3:
                return HandType.THREE_OF_A_KIND
            if cardCountList[-1] == 2:
                return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    def classifyHandTypeWithJokers(self, hand: str):
        localHand = "".join(a for a in hand if a != 'J')
        handType = self.classifyHandType(localHand)

        for _ in range(hand.count('J')):
            handType = self.handTypeTransitionMap[handType]

        return handType

    def partCommon(self, cardMap: dict, evaluator):
        handInfoList = list((evaluator(a[0]),
                             tuple(cardMap[b] for b in a[0]), *a)
                            for a in self.handList)
        handInfoList.sort(key=lambda a: (a[0].value, a[1]))
        return sum((i+1) * a[3] for i, a in enumerate(handInfoList))

    def part1(self):
        cardMap = {str(a): a for a in range(2, 10)}
        cardMap.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})
        return self.partCommon(cardMap, self.classifyHandType)

    def part2(self):
        cardMap = {str(a): a for a in range(2, 10)}
        cardMap.update({'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14})
        return self.partCommon(cardMap, self.classifyHandTypeWithJokers)


class TestCase(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.handImpl = Implementation(f'2023/data/{__name__}_example.txt')

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 6440)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        # below is too high
        self.assertEqual(result, 248836197)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 5905)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 251195607)
