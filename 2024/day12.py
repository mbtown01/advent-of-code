import unittest
from os import path


class Implementation:
    # For a given vector, provide the relative corners of the far edge
    # of a given cell (e.g., traveling north would yielf the north edge)
    vecEdgePairMap = {(-1, 0): ((0, 0), (0, 1)),
                      (0, 1): ((0, 1), (1, 1)),
                      (1, 0): ((1, 1), (1, 0)),
                      (0, -1): ((1, 0), (0, 0))}
    # For a given vector, provide the order in which to test for edges in the
    # set of edges so to keep traveling clockwise (always right-hand turns)
    # (e.g., traveling north would test east, then south, then west)
    vecTurnOptionsMap = {(-1, 0): ((0, 1), (-1, 0), (0, -1)),
                         (0, 1): ((1, 0), (0, 1), (-1, 0)),
                         (1, 0): ((0, -1), (1, 0), (0, 1)),
                         (0, -1): ((-1, 0), (0, -1), (1, 0))}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}

        # Find all polygon edges and associate with the grid location and
        # value that would be INSIDE that polygon
        edgeMap = dict()
        for loc, val in self.gridMap.items():
            for vec, (v1, v2) in self.vecEdgePairMap.items():
                nextLoc = (loc[0]+vec[0], loc[1]+vec[1])
                if val != self.gridMap.get(nextLoc, 'BOUNDARY'):
                    p1 = (loc[0]+v1[0], loc[1]+v1[1])
                    p2 = (loc[0]+v2[0], loc[1]+v2[1])
                    edgeMap[(p1, p2)] = loc, val

        # Given the edgeMap, pull a random edge out and walk that edge
        # clock-wise until the walk returns to start, yielding a polygon
        self.resultList = list()
        while len(edgeMap) > 0:
            (v1, v2), (loc, val) = edgeMap.popitem()
            vList = [v1, v2]
            while vList[-1] != vList[0]:
                v1, v2 = vList[-2:]
                vec = (v2[0]-v1[0], v2[1]-v1[1])
                for v3 in self.vecTurnOptionsMap[vec]:
                    vNext = (v2[0]+v3[0], v2[1]+v3[1])
                    if edgeMap.pop((v2, vNext), None) is not None:
                        vList.append(vNext)
                        break

            # Using the first loc as a starting point, flood-fill the
            # polygon to find all the contained locations
            frontier, locSet = [loc], set([loc])
            while len(frontier) > 0:
                loc = frontier.pop(0)
                for vec in self.vecEdgePairMap:
                    nextLoc = (loc[0]+vec[0], loc[1]+vec[1])
                    if nextLoc not in locSet:
                        if val == self.gridMap.get(nextLoc, 'BOUNDARY'):
                            locSet.add(nextLoc)
                            frontier.append(nextLoc)

            # Eliminate any vertices that are part of a straight line
            vList, sideList = vList[:-1], list()
            convList = vList[-1:] + vList[:-1], vList, vList[1:] + vList[:1]
            for v1, v2, v3 in zip(*convList):
                if (v2[0]-v1[0], v2[1]-v1[1]) != (v3[0]-v2[0], v3[1]-v2[1]):
                    sideList.append(v2)

            self.resultList.append((vList, sideList, len(locSet)))

    def part1(self):
        return sum((len(a))*b for (a, _, b) in self.resultList)

    def part2(self):
        return sum((len(a))*b for (_, a, b) in self.resultList)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 1930)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1450816)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 1206)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 865662)
