import unittest
from collections import defaultdict


class TileInfo:

    def __init__(self) -> None:
        self.seenLocMap = dict()
        self.occupiedCount = 0
        self.displayChar = None
        self.firstSeenEvenOddCounts = [0, 0]
        self.stepCountMap = dict()
        self.minStep = 1024*1024
        self.maxStep = -1

    def __hash__(self) -> int:
        return hash(tuple(self.seenLocMap.keys()))

    def getActiveLocCount(self, step: int, minStep: int = None):
        localMinStep = self.minStep if minStep is None else minStep
        localStep = step - localMinStep
        if localStep < 0:
            return 0
        locCount = self.stepCountMap.get(localStep)
        if locCount is not None:
            return locCount
        return self.firstSeenEvenOddCounts[localStep % 2]

    def getActiveLocSequence(self):
        return list(self.stepCountMap.values())

    def stepOutOf(self):
        self.occupiedCount -= 1

    def stepInto(self, step: int, relLoc: tuple):
        self.seenLocMap[relLoc] = True
        self.minStep = min(self.minStep, step)
        self.maxStep = max(self.maxStep, step)
        localStep = step - self.minStep
        self.firstSeenEvenOddCounts[localStep % 2] += 1
        self.stepCountMap[localStep] = \
            self.firstSeenEvenOddCounts[localStep % 2]
        self.occupiedCount += 1


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            textRowList = list(a.strip() for a in reader)

        self.rowCount = len(textRowList)
        self.colCount = len(textRowList[0])
        self.startLoc = (self.rowCount // 2, self.colCount // 2)
        self.nodeMap = {
            (j, i): c
            for j, row in enumerate(textRowList)
            for i, c in enumerate(row.strip())
        }

        assert 'S' == self.nodeMap[self.startLoc]
        self.nodeMap[self.startLoc] = '.'

    def _getBoundingRangeValues(self, tupleList: list):
        jValues = list(a[0] for a in tupleList)
        iValues = list(a[1] for a in tupleList)
        return min(jValues), max(jValues), min(iValues), max(iValues)

    def _sanityCheck(self, tileInfoMap: dict, steps: int, zzTestMap: dict):
        axisFwd, axisBkwd, axisConst = (1, 12), (-1, -12, -1), (1,)
        axisRanges = [[axisFwd, axisConst], [axisConst, axisFwd],
                      [axisBkwd, axisConst], [axisConst, axisBkwd]]
        for jBounds, iBounds in axisRanges:
            allTiles = list(tileInfoMap[(j, i)]
                            for j in range(*jBounds)
                            for i in range(*iBounds)
                            if (j, i) in tileInfoMap)
            total = sum(a.getActiveLocCount(steps) for a in allTiles)
            if len(allTiles) > 2:
                axisChar = allTiles[-3].displayChar
                print(f"AXES [{axisChar}] REAL = {total}")
                print(f"AXES [{axisChar}] TEST = {zzTestMap.get(axisChar)}")

        axisFwd, axisBkwd = (1, 12), (-1, -12, -1)
        axisRanges = [[axisFwd, axisFwd], [axisFwd, axisBkwd],
                      [axisBkwd, axisFwd], [axisBkwd, axisBkwd]]
        for jBounds, iBounds in axisRanges:
            allTiles = list(tileInfoMap[(j, i)]
                            for j in range(*jBounds)
                            for i in range(*iBounds)
                            if (j, i) in tileInfoMap)
            total = sum(a.getActiveLocCount(steps) for a in allTiles)
            if len(allTiles) > 0:
                axisChar = allTiles[0].displayChar
                print(f"DIAG [{axisChar}] REAL = {total}")
                print(f"AXES [{axisChar}] TEST = {zzTestMap.get(axisChar)}")
                for j in range(*jBounds):
                    temp = list(tileInfoMap[(j, i)]
                                for i in range(*iBounds)
                                if (j, i) in tileInfoMap)
                    data = list(str(a.getActiveLocCount(steps)) for a in temp)
                    print(' '.join(data))

    def _dump(self, completedTileInfoMap: dict, step: int):
        jMin, jMax, iMin, iMax = \
            self._getBoundingRangeValues(completedTileInfoMap.keys())

        for j in range(jMin, jMax+1):
            rowChars = ' '.join(list(
                completedTileInfoMap[(j, i)].displayChar
                if (j, i) in completedTileInfoMap else ' '
                for i in range(iMin, iMax+1)))
            print(f"[{j:04d}]  {rowChars}")
        print(f"step = {step}")

    def findAll(self, steps: int):
        tileInfoMap = defaultdict(TileInfo)
        tileInfoMap[(0, 0)].stepInto(0, self.startLoc)
        occupiedLocList = [self.startLoc]
        completedTileInfoMap, refHashTileInfoMap = {}, {}

        # Once a node has been seen, it simply toggles on/off forever.
        # We only propagate the 'wave front' below, and can guess the state
        # of any timestep based on if it was odd/even
        for step in range(steps):
            lastOccupiedLocList, occupiedLocList = occupiedLocList, list()
            for currLoc in lastOccupiedLocList:
                currTile = (currLoc[0] // self.rowCount,
                            currLoc[1] // self.colCount)
                tileInfoMap[currTile].stepOutOf()

                for delta in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nextLoc = (currLoc[0] + delta[0],
                               currLoc[1] + delta[1])
                    nextRelLoc = (nextLoc[0] % self.rowCount,
                                  nextLoc[1] % self.colCount)
                    nextTile = (nextLoc[0] // self.rowCount,
                                nextLoc[1] // self.colCount)
                    if self.nodeMap[nextRelLoc] == '.' and \
                            nextRelLoc not in tileInfoMap[nextTile].seenLocMap:
                        tileInfoMap[nextTile].stepInto(step+1, nextRelLoc)
                        occupiedLocList.append(nextLoc)

            # Check to see if we've completely finished a tile and if so,
            # build a unique hash for the ORDER in which nodes were visited
            noLongerOccupiedTileList = list(
                a for a, b in tileInfoMap.items() if b.occupiedCount == 0)
            for tile in noLongerOccupiedTileList:
                tileInfo = tileInfoMap[tile]
                refTileInfo = refHashTileInfoMap.get(hash(tileInfo))
                if refTileInfo is None:
                    tileInfo.displayChar = \
                        chr(ord('A') + len(refHashTileInfoMap))
                    refHashTileInfoMap[hash(tileInfo)] = tileInfo
                    refTileInfo = tileInfo
                tileInfo.displayChar = refTileInfo.displayChar
                completedTileInfoMap[tile] = tileInfo

            # If ANY tiles were finished, check whether we are repeating
            # in any of the cardinal directions and if so, do some fancy
            # math to predict the final valuef
            zzTestMap = dict()
            if len(noLongerOccupiedTileList) > 0 and len(tileInfoMap) > 9:
                axisGoodCount, totalActiveLocCount = 0, 0
                jMin, jMax, iMin, iMax = \
                    self._getBoundingRangeValues(completedTileInfoMap.keys())
                self._dump(completedTileInfoMap, step)

                # Check whether each of the 4 cardinal axes has started
                # repeating and if they have, we can now calcuate forward
                compAxisTileInfolist = [
                    list(tileInfoMap[(j, 0)] for j in range(1, jMax+1)),
                    list(tileInfoMap[(j, 0)] for j in range(-1, jMin-1, -1)),
                    list(tileInfoMap[(0, i)] for i in range(1, iMax+1)),
                    list(tileInfoMap[(0, i)] for i in range(-1, iMin-1, -1))]
                for axis in compAxisTileInfolist:
                    if len(axis) <= 2 or hash(axis[-1]) != hash(axis[-2]):
                        break

                    axisStepPace = axis[-1].minStep - axis[-2].minStep
                    nextStep = axis[-1].minStep + axisStepPace
                    pairsRemain = (steps - nextStep) // axisStepPace // 2 - 1
                    nextStep += pairsRemain * axisStepPace * 2

                    axisActiveLocCountList = \
                        list(a.getActiveLocCount(steps) for a in axis)
                    axisActiveLocCount = \
                        sum(axisActiveLocCountList) + \
                        pairsRemain * sum(axisActiveLocCountList[-2:])
                    while nextStep < steps:
                        axisActiveLocCount += \
                            axis[-1].getActiveLocCount(steps, nextStep)
                        nextStep += axisStepPace

                    zzTestMap[axis[-3].displayChar] = axisActiveLocCount
                    totalActiveLocCount += axisActiveLocCount
                    axisGoodCount += 1

                # Now check whether the four wedges going NE, NW, SE, SW
                # are repeating and if so, we can calculate this forward too
                testRanges = [
                    list((j, -1) for j in range(1, jMax+1)),
                    list((j, 1) for j in range(-1, jMin-1, -1)),
                    list((1, i) for i in range(1, iMax+1)),
                    list((-1, i) for i in range(-1, iMin-1, -1))]
                diagAxisTileInfoList = list(
                    list(tileInfoMap[a] for a in r if a in tileInfoMap)
                    for r in testRanges)
                for axis in diagAxisTileInfoList:
                    if len(axis) <= 2 or hash(axis[-1]) != hash(axis[-2]):
                        break

                    axisStepPace = axis[-1].minStep - axis[-2].minStep
                    nextStep = axis[0].minStep
                    pairsRemain = (steps - nextStep) // axisStepPace // 2 - 1
                    nextStep += pairsRemain * axisStepPace * 2

                    axisActiveLocCountList = \
                        list(a.getActiveLocCount(steps) for a in axis)
                    oddAxisLocCount = pairsRemain * (2*(pairsRemain+1)//2 - 1)
                    evenAxisLocCount = pairsRemain * 2*(pairsRemain+1)//2
                    axisActiveLocCount = \
                        oddAxisLocCount * axisActiveLocCountList[0] + \
                        evenAxisLocCount * axisActiveLocCountList[1]
                    width = 2 * pairsRemain + 1
                    while nextStep <= steps:
                        locCount = axis[-1].getActiveLocCount(steps, nextStep)
                        axisActiveLocCount += locCount * width
                        nextStep += axisStepPace
                        width += 1

                    zzTestMap[axis[0].displayChar] = axisActiveLocCount
                    totalActiveLocCount += axisActiveLocCount
                    axisGoodCount += 1

                if axisGoodCount == 8:
                    return totalActiveLocCount + \
                        tileInfoMap[(0, 0)].getActiveLocCount(steps)

        self._sanityCheck(tileInfoMap, steps, zzTestMap)

        # If we got to here, we just do it the old fashioned way!!
        return sum(a.getActiveLocCount(steps) for a in tileInfoMap.values())

    def part1(self, steps: int):
        return self.findAll(steps)

    def part2(self, steps: int):
        return self.findAll(steps)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1(6)
        self.assertEqual(result, 16)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1(64)
        self.assertEqual(result, 3651)

    def test_part2_ex_10(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(10), 50)

    def test_part2_ex_50(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(50), 1594)

    def test_part2_ex_100(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(100), 6536)

    def test_part2_ex_101(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(101), 6684)

    def test_part2_ex_500(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(500), 167004)

    def test_part2_ex_1000(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(1000), 668697)

    def test_part2_ex_5000(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        self.assertEqual(impl.part2(5000), 16733044)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        self.assertEqual(impl.part2(26501365), 607334325965751)
