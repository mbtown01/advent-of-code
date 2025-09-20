import unittest
from os import path
from collections import defaultdict

GSIZE = 10
EDGE_INDICES = [list((0, i) for i in range(GSIZE)),
                list((j, GSIZE-1) for j in range(GSIZE)),
                list((GSIZE-1, i) for i in range(GSIZE)),
                list((j, 0) for j in range(GSIZE))]


class Implementation:

    class Grid:

        def __init__(self, dataMap: dict):
            self.dataMap = dataMap
            self.edgeHashMap = dict()
            self.maxExtents = max(self.dataMap.keys())
            assert (0, 0) == min(self.dataMap.keys())

            for edge, edgeIndices in enumerate(EDGE_INDICES):
                edgeHash = sum(2**i if self.dataMap[index] == '#' else 0
                               for i, index in enumerate(edgeIndices))
                self.edgeHashMap[edge] = edgeHash

        def rotate(self):
            nj, _ = self.maxExtents
            dataMap = {(i, nj-j): c for (j, i), c in self.dataMap.items()}
            return Implementation.Grid(dataMap)

        def flip(self):
            _, ni = self.maxExtents
            dataMap = {(j, ni-i): c for (j, i), c in self.dataMap.items()}
            return Implementation.Grid(dataMap)

        def dump(self):
            print()
            minExtents = min(self.dataMap.keys())
            maxExtents = max(self.dataMap.keys())
            for y in range(maxExtents[0] - minExtents[0] + 1):
                charList = list(self.dataMap[(y, x)]
                                for x in range(maxExtents[1] - minExtents[1] + 1))
                print(f"[{y:02d}] {' '.join(charList)}")

    def __init__(self, dataPath: str):
        self.gridMap = defaultdict(dict)

        with open(dataPath, encoding="utf8") as reader:
            allLines = list(a.strip() for a in reader.readlines())

        # Build all the grids
        for i in list(i for i, l in enumerate(allLines) if 'Tile' in l):
            gridId = int(allLines[i].split(' ')[1].split(':')[0])
            dataMap = {(j, i): c
                       for j, line in enumerate(allLines[i+1:i+GSIZE+1])
                       for i, c in enumerate(line)}
            grid = Implementation.Grid(dataMap)

            for flips in range(2):
                for rotations in range(4):
                    state = (flips, rotations)
                    self.gridMap[gridId][state] = grid
                    grid = grid.rotate()
                grid = grid.flip()

        # Match all the grid edges based on state
        hashToEdgesMap = defaultdict(list)
        for gridId, stateMap in self.gridMap.items():
            for state, grid in stateMap.items():
                for edge, edgeHash in grid.edgeHashMap.items():
                    hashToEdgesMap[edgeHash].append((gridId, state, edge))

        edgeMatch = {0: 2, 1: 3, 2: 0, 3: 1}
        gridMatchMap = defaultdict(dict)
        for outEdgeList in hashToEdgesMap.values():
            gridIdMap = {a[0]: 1 for a in outEdgeList}
            if len(gridIdMap) == 2:
                for i, a in enumerate(outEdgeList[:-1]):
                    for b in outEdgeList[i+1:]:
                        if a[0] != b[0] and a[2] == edgeMatch[b[2]]:
                            gridMatchMap[a[0]][a] = b
                            gridMatchMap[b[0]][b] = a

        # pick any gridId and walk each of the 8 possible states.  this approach
        # only works because every edge hash unique!!
        edgePosDelta = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        gridPosMap = defaultdict(dict)
        gridEdgeMatchList = list((a, len(b)) for a, b in gridMatchMap.items())
        refGridId = sorted(gridEdgeMatchList, key=lambda a: a[1])[-1][0]
        workQueue = [(refGridId, (0, 0), (0, 0))]
        while len(workQueue):
            gridId, state, pos = workQueue.pop(0)
            gridPosMap[pos] = (gridId, state)
            for edge in range(4):
                nextPos = tuple(a+b for a, b in zip(pos, edgePosDelta[edge]))
                match = gridMatchMap[gridId].get((gridId, state, edge))
                if match is not None and nextPos not in gridPosMap:
                    workQueue.append((match[0], match[1], nextPos))

        minPos = min(gridPosMap.keys())
        self.gridPosMap = {(a[0]-minPos[0], a[1]-minPos[1]): b
                           for a, b in gridPosMap.items()}
        self.gridPosExtents = max(self.gridPosMap.keys())

    def part1(self):
        maxX, maxY = self.gridPosExtents
        cornerPosList = [(0, 0), (0, maxX), (maxY, 0), (maxY, maxX)]
        corners = list(self.gridPosMap[i][0] for i in cornerPosList)
        return corners[0] * corners[1] * corners[2] * corners[3]

    def part2(self):
        monster = ["                  # ",
                   "#    ##    ##    ###",
                   " #  #  #  #  #  #   "]
        monsterMap = {(y, x): '#'
                      for y, l in enumerate(monster)
                      for x, c in enumerate(l)
                      if c == '#'}

        bigGrid = dict()
        for (y, x), (gridId, state) in self.gridPosMap.items():
            grid = self.gridMap[gridId][state].dataMap
            for yy in range(GSIZE-2):
                for xx in range(GSIZE-2):
                    bigGrid[(y*(GSIZE-2)+yy, x*(GSIZE-2)+xx)] = \
                        grid[(yy+1, xx+1)]

        bigGrid = Implementation.Grid(bigGrid)
        resultGrid = Implementation.Grid(bigGrid.dataMap.copy())

        for _ in range(2):
            for _ in range(4):
                for bp in bigGrid.dataMap.keys():
                    if all(bigGrid.dataMap.get((bp[0]+mp[0], bp[1]+mp[1]), '') == '#'
                           for mp in monsterMap.keys()):
                        for mp in monsterMap.keys():
                            resultGrid.dataMap[(
                                bp[0]+mp[0], bp[1]+mp[1])] = 'M'

                bigGrid = bigGrid.rotate()
                resultGrid = resultGrid.rotate()
            bigGrid = bigGrid.flip()
            resultGrid = resultGrid.flip()

        return sum(v == '#' for v in resultGrid.dataMap.values())


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def unique(self, impl, tiles):
        test, real = defaultdict(dict), 2*tiles*(tiles-1)
        for a in impl.allOutEdges:
            test[a[4]][a[0]] = 1
        test = {a: b for a, b in test.items() if len(b) > 1}

        self.assertEqual(real, len(test) // 2)

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 20899048083289)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 4006801655873)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 273)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1838)
