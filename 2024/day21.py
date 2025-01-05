import unittest
from os import path
from itertools import product
from collections import defaultdict


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.codeList = list(a.strip() for a in reader)
            self.bestSeqListMap = defaultdict(list)

            self.updateBestSeqMapForKeypad([' ^A', '<v>'])
            self.updateBestSeqMapForKeypad(['789', '456', '123', ' 0A'])

    def updateBestSeqMapForKeypad(self, keyRowList: list):
        gridKeyMap = {c: (j, i)
                      for j, line in enumerate(keyRowList)
                      for i, c in enumerate(line)}
        validKeyList = list(a for a in gridKeyMap if a != ' ')
        charVecMap = {'^': (-1, 0), '>': (0, 1), '<': (0, -1), 'v': (1, 0)}
        spaceLoc = next(b for a, b in gridKeyMap.items() if a == ' ')

        for startKey, destKey in product(validKeyList, repeat=2):
            startLoc, destLoc = gridKeyMap[startKey], gridKeyMap[destKey]
            delta = (destLoc[0]-startLoc[0], destLoc[1]-startLoc[1])
            baseSequence = ''.join(
                c for c, d in charVecMap.items()
                for dim in range(2) for _ in range(abs(delta[dim]))
                if d[dim] != 0 and delta[dim] // d[dim] == abs(delta[dim]))
            for sequence in set([baseSequence, baseSequence[::-1]]):
                locList = [startLoc]
                for seqChar in sequence:
                    locList.append((locList[-1][0]+charVecMap[seqChar][0],
                                    locList[-1][1]+charVecMap[seqChar][1]))
                if spaceLoc not in locList:
                    self.bestSeqListMap[(startKey, destKey)].append(sequence)

    def search(self, code: str, depth: int, *, cache: dict = None):
        cache, cacheKey = dict() if cache is None else cache, (code, depth)
        result = cache.get(cacheKey, 0)
        if result == 0:
            for startKey, destKey in zip('A'+code[:-1], code):
                seqList = self.bestSeqListMap[(startKey, destKey)]
                result += len(seqList[0])+1 if depth == 0 \
                    else min(self.search(seq+'A', depth-1, cache=cache)
                             for seq in seqList)
            cache[cacheKey] = result

        return result

    def part1(self):
        return sum(int(c[:-1]) * self.search(c, 2) for c in self.codeList)

    def part2(self):
        return sum(int(c[:-1]) * self.search(c, 25) for c in self.codeList)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 126384)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 188398)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 230049027535970)
