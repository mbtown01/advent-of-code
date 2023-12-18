
class Span:

    def __init__(self, start: int, *, length: int = None):
        self.start = start
        self.end = start + length - 1
        self.length = length

    def __repr__(self) -> str:
        return f"[Span ({self.start}-{self.end}) len={self.length}]"

    @property
    def points(self):
        return [self.start, self.end]

    def containsPoint(self, value: int):
        return self.start <= value <= self.end


class SourceDestinationMap:

    def __init__(self, srcName: str, destName: str) -> None:
        self.srcName = srcName
        self.destName = destName
        self.spanMappingDict = {}

    def __repr__(self) -> str:
        return f"[SourceDestinationMapping {self.srcName} -> {self.destName}]"

    def addSpanMapping(self, destStart: int, srcStart: int, length: int):
        srcSpan = Span(srcStart, length=length)
        destSpan = Span(destStart, length=length)
        assert srcSpan not in self.spanMappingDict
        self.spanMappingDict[srcSpan] = destSpan

    def getForwardMapping(self, point: int):
        for src, dest in self.spanMappingDict.items():
            if src.containsPoint(point):
                return dest.start + (point-src.start)
        return point

    def getReverseMapping(self, point: int):
        for src, dest in self.spanMappingDict.items():
            if dest.containsPoint(point):
                return src.start + (point-dest.start)
        return point

    def getForwardKeyPointsSet(self,
                               prevMapping: "SourceDestinationMap",
                               keyPointsSet: set):
        result = set(self.getForwardMapping(a) for a in keyPointsSet)
        pointSet = set(self.getForwardMapping(p)
                       for s in self.spanMappingDict
                       for m in prevMapping.spanMappingDict.values()
                       for p in [s.start-1, *s.points, s.end+1]
                       if m.containsPoint(p))
        return result.union(pointSet)


class Implementation:

    def __init__(self, dataPath: str = '2023/day5_test.txt'):
        with open(dataPath, encoding="utf8") as reader:
            self.seedList, self.mappingList = [], []
            for line in reader:
                line = line.strip()
                if line.startswith('seeds:'):
                    _, numberText = line.split(': ')
                    self.seedList += list(
                        int(a) for a in numberText.split(' '))
                if line.endswith('map:'):
                    name, _ = line.split(' ')
                    srcName, _, destName = name.split('-')
                    self.mappingList.append(
                        SourceDestinationMap(srcName, destName))
                if len(line) and line[0] in '0123456789':
                    destStart, srcStart, length = (
                        int(a) for a in line.split(' '))
                    self.mappingList[-1].addSpanMapping(
                        destStart, srcStart, length)

            self.seedMapping = SourceDestinationMap('seed', 'seed')
            for i in range(0, len(self.seedList), 2):
                self.seedMapping.addSpanMapping(
                    self.seedList[i], self.seedList[i], self.seedList[i+1])

    def part1(self):
        seedMappingList = list([a, a] for a in self.seedList)
        for seedLocationPair in seedMappingList:
            for mapping in self.mappingList:
                seedLocationPair[1] = mapping.getForwardMapping(
                    seedLocationPair[1])

        return sorted(seedMappingList, key=lambda a: a[1])[0]

    def part2(self):
        prevMapping = self.seedMapping
        keyPointsSet = set(prevMapping.getForwardMapping(a)
                           for b in prevMapping.spanMappingDict
                           for a in b.points)
        for thisMapping in self.mappingList:
            keyPointsSet = thisMapping.getForwardKeyPointsSet(
                prevMapping, keyPointsSet)
            prevMapping = thisMapping

        keyPointsMap = {a: a for a in keyPointsSet}
        for thisMapping in self.mappingList[::-1]:
            update = {a: thisMapping.getReverseMapping(b)
                      for a, b in keyPointsMap.items()}
            keyPointsMap.update(update)

        result = {b: a for a, b in keyPointsMap.items()
                  for m in self.seedMapping.spanMappingDict
                  if m.containsPoint(b)}
        return sorted(result.items(), key=lambda a: a[1])[0]


if __name__ == "__main__":
    impl = Implementation()
    print(f"part 1: {impl.part1()}")
    print(f"part 2: {impl.part2()}")
