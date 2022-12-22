

class Valve:
    def __init__(self, name: str, rate: int):
        self.name = name
        self.rate = rate
        self.tunnelToValveList = list()
        self.valveHopMap = {self: []}

    def __repr__(self) -> str:
        return f"[Valve '{self.name} rate={self.rate}']"

    def init(self):
        self._initValveHopMap(self.valveHopMap, [])
        self.valveHopMap = \
            {a: b for a, b in self.valveHopMap.items() if a.rate > 0}

    def _initValveHopMap(self, valveHopMap: dict, path: list):
        valvesToSearch = list()
        for valve in self.tunnelToValveList:
            prevPath = valveHopMap.get(valve)
            if prevPath is None or len(path) < len(prevPath):
                valveHopMap[valve] = path + [valve]
                valvesToSearch.append(valve)
        for valve in valvesToSearch:
            valve._initValveHopMap(valveHopMap, path + [valve])


def findBestPath(
        v1: Valve, v2: Valve, p1: list, p2: list, rate: int,
        best: int, max: int, opened: dict, remains: int):
    v1, v2, p1, p2 = v2, v1, p2, p1

    if v1 is None:
        return findBestPath(
            v1, v2, p1, p2, rate, best, max, opened, remains-1)
    if remains <= 0 or max == 0 or (rate + max*(remains // 2 - 1)) < best:
        return rate, opened
    if len(p1) > 0:
        return findBestPath(
            p1[0], v2, p1[1:], p2, rate, best, max, opened, remains-1)
    if v1.rate > 0 and v1 not in opened:
        rate = rate + v1.rate * (remains // 2 - 1)
        max = max - v1.rate
        opened = {**opened, v1: 31 - remains//2}
        return findBestPath(
            v1, v2, p1, p2, rate, best, max, opened, remains-1)

    bestRate, bestOpened = best, {}
    for nextValve, nextPath in v1.valveHopMap.items():
        if nextValve not in opened:
            nextRate, nextOpened = findBestPath(
                nextValve, v2, nextPath[1:], p2, rate, bestRate, max, opened, remains-1)
            if nextRate > bestRate:
                bestRate, bestOpened = (nextRate, nextOpened)

    return bestRate, bestOpened


valveList, valveMap = list(), dict()
with open('2022/day16.txt') as reader:
    allLines = reader.readlines()
    for line in allLines:
        parts = line.strip().replace(';', '').split(' ')
        rate = int(parts[4].split('=')[1])
        valveMap[parts[1]] = Valve(parts[1], rate)
        valveList.append(valveMap[parts[1]])
    for line in allLines:
        parts = line.strip().replace(',', '').split(' ')
        for nextValve in parts[9:]:
            valveMap[parts[1]].tunnelToValveList.append(valveMap[nextValve])
    for valve in valveList:
        valve.init()

max = sum(a.rate for a in valveList)
result = findBestPath(
    None, valveMap['AA'], [], [], 0, 0, max, {}, 30*2+1)
print(f"part 1a [Test]: {result[0]}")

# Seed the 2nd search knowing the BEST result we've seen so far is the
# single-person tunnel search.  This massively reduces the search space.
# Still takes a minute or two...
result = findBestPath(
    valveMap['AA'], valveMap['AA'], [], [], 0, result[0], max, {}, 26*2+1)
print(f"part 2: {result[0]}")
