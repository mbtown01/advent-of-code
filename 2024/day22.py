import unittest
from os import path
from collections import defaultdict


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.secretValList = list(int(a.strip()) for a in reader)

    def calcNextSecretVal(self, secretVal: int):
        secretVal = ((secretVal * 2**6) ^ secretVal) % 2**24
        secretVal = ((secretVal // 2**5) ^ secretVal) % 2**24
        secretVal = ((secretVal * 2**11) ^ secretVal) % 2**24
        return secretVal

    def buildBuyerNumList(self):
        buyerNumList = list([v]*2001 for v in self.secretValList)
        for buyerList in buyerNumList:
            for i in range(2000):
                buyerList[i+1] = self.calcNextSecretVal(buyerList[i])
        return buyerNumList

    def part1(self):
        buyerNumList = self.buildBuyerNumList()
        return sum(buyerList[-1] for buyerList in buyerNumList)

    def part2(self):
        buyerNumList = self.buildBuyerNumList()
        buyerSeqResultList = list(dict() for _ in range(len(buyerNumList)))
        for buyer, l in enumerate(buyerNumList):
            d = list((b % 10 - a % 10) for a, b in zip(l[:-1], l[1:]))
            for i, seq in enumerate(zip(d[:-3], d[1:-2], d[2:-1], d[3:])):
                if seq not in buyerSeqResultList[buyer]:
                    buyerSeqResultList[buyer][seq] = l[i+4] % 10

        finalResult = defaultdict(int)
        for buyerSeqResult in buyerSeqResultList:
            for seq, result in buyerSeqResult.items():
                finalResult[seq] += result

        return max(finalResult.items(), key=lambda a: a[1])[1]


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 37327623)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 13185239446)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example2.txt')
        result = impl.part2()
        self.assertEqual(result, 23)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1501)
