import unittest
from os import path
from collections import defaultdict
from itertools import combinations


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.networkMap = defaultdict(list)
            self.edgeList = list()
            for line in reader:
                a, b = line.strip().split('-')
                self.edgeList.append([a, b])
                self.networkMap[a].append(b)
                self.networkMap[b].append(a)

    def buildThreeWayClusterSet(self):
        return set(list(
            tuple(sorted((n1, n2, n3)))
            for n1, n2 in self.edgeList
            for n3 in self.networkMap[n1]
            if n3 in self.networkMap[n2] and n2 in self.networkMap[n3]))

    def part1(self):
        clusterSet = self.buildThreeWayClusterSet()
        return sum(any(a[0] == 't' for a in z) for z in clusterSet)

    def part2(self):
        currClusterSet = self.buildThreeWayClusterSet()
        while len(currClusterSet) > 1:
            currClusterSet = set(list(
                tuple(sorted([node, *cluster]))
                for cluster in currClusterSet
                for node in self.networkMap[cluster[0]]
                if node not in cluster and
                all(node in self.networkMap[a] for a in cluster)
            ))

        return ','.join(list(currClusterSet)[0])


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 7)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1238)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 'co,de,ka,ta')

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 'bg,bl,ch,fn,fv,gd,jn,kk,lk,pv,rr,tb,vw')
