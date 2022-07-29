from collections import defaultdict
from enum import Enum


class Burrow:

    def __init__(self, name: str) -> None:
        self.name = name


class Node:

    def __init__(self, index: int, burrow: Burrow):
        self.index = index
        self.edges = list()
        self.nodePaths = dict()
        self.canStop = None
        self.burrow = burrow

    def __repr__(self) -> str:
        return f"[Node {self.index} edges={len(self.edges)} {self.canStop}]"

    @property
    def isBurrow(self):
        return self.burrow is not None

    def _analyzeGraph(self, nodePaths: dict, path: list):
        for node in (a.destination for a in self.edges):
            if node not in path:
                thisPath = path + [node]
                if node.canStop:
                    nodePaths[node] = thisPath
                node._analyzeGraph(nodePaths, thisPath)

    def analyzeGraph(self):
        self._analyzeGraph(self.nodePaths, [self])
        return None

    def initializeEdges(self):
        self.canStop = len(self.edges) != 3


class Edge:

    class Direction(Enum):
        NORTH = 1
        SOUTH = 2
        EAST = 3
        WEST = 4

    def __init__(self, destination: Node, dir: Direction):
        self.destination = destination
        self.direction = dir

    @classmethod
    def connect(cls, a: Node, aDir: Direction, b: Node, bDir: Direction):
        a.edges.append(Edge(b, bDir))
        b.edges.append(Edge(a, aDir))

    def __repr__(self) -> str:
        return f"[Edge to {self.destination} dir={self.direction}]"


class Anthropod:

    ENERGY_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    def __init__(self, name: str, start: Node, destination: Node):
        self.name = name
        self.energySpent = 0
        self.energyPerMove = self.ENERGY_MAP[name]
        self.start = start
        self.destination = destination
        self._hasMoved = False
        self._moveInfo = dict()

    def __repr__(self) -> str:
        return (f"[Anthropod '{self.name}' "
                f"hasMoved={self._hasMoved} "
                f"moves={len(self._moveInfo)}"
                f"]")

    @property
    def hasMoves(self):
        return len(self._moveInfo) > 0

    def _computeNeedsToMove(self, anthropodLocations: list):
        if self.start != self.destination:
            return True

        southernEdgeList = list(
            a for a in self.start.edges if a.direction == Edge.Direction.SOUTH)
        if len(southernEdgeList) == 0:
            return False

        southernNeighborIndex = southernEdgeList[0].destination.index
        southernNeighbor = anthropodLocations[southernNeighborIndex]
        return southernNeighbor._computeNeedsToMove(anthropodLocations)

    def initializeMoves(self, anthropodLocations: list):
        if self._computeNeedsToMove(anthropodLocations):
            hallwayNodeInfo = list(
                a for a in self.start.nodePaths.items() if not a[0].isBurrow)
            for hallwayNode, path1 in hallwayNodeInfo:
                path2 = hallwayNode.nodePaths[self.destination]
                energy = (len(path1) + len(path2) - 2) * self.energyPerMove
                self._moveInfo[hallwayNode] = \
                    dict(path1=path1, path2=path2, energy=energy)

            # In the case where we are at our final destination but we still
            # need to move out of the way, a straight-shot home is NOT a
            # possible move, so filter that out
            if self.destination in self.start.nodePaths:
                path1 = self.start.nodePaths[self.destination]
                energy = (len(path1) - 1) * self.energyPerMove
                self._moveInfo[self.destination] = \
                    dict(path1=path1, path2=None, energy=energy)

    def getAvailableMoves(self, nodes: list, anthropodLocations: list):
        location = nodes[anthropodLocations.index(self)]
        occupiedNodes = set(
            a for a, b in zip(nodes, anthropodLocations) if b is not None)
        if not location.isBurrow:
            return [self._moveInfo[location]['path2']]

        moveInfoList = sorted(list(self._moveInfo.values()),
                              key=lambda a: a['energy'])
        return list(a['path1'] for a in moveInfoList
                    if len(occupiedNodes.intersection(a['path1']) == 0))


class Game:

    def __init__(self, state: str):
        self.burrows = list(Burrow(a) for a in 'ABCD')
        self.nodes = list(Node(index, None) for index in range(11))
        self.nodes += list(
            Node(i+11, b) for i, b in enumerate(self.burrows + self.burrows))
        for a, b in zip(self.nodes[0:10], self.nodes[1:11]):
            Edge.connect(a, Edge.Direction.WEST, b, Edge.Direction.EAST)
        for b in range(4):
            Edge.connect(self.nodes[2*(b+1)], Edge.Direction.NORTH,
                         self.nodes[11+b], Edge.Direction.SOUTH)
            Edge.connect(self.nodes[11+b], Edge.Direction.NORTH,
                         self.nodes[11+b+4], Edge.Direction.SOUTH)

        destinations = defaultdict(list)
        for a, b in zip('ABCDABCD', self.nodes[11:]):
            destinations[a].append(b)

        # Assumption is that it is NOT important which final destination
        # (top or bottom of burrow) any anthropod takes.  HOWEVER, if an
        # anthropod is ALREADY in the bottom position, then THAT needs to
        # be it's final destination
        self.anthropods = list()
        for a, b in zip(state, self.nodes[11:]):
            i = destinations[a].index(b) if b in destinations[a] else 0
            anthropod = Anthropod(a, b, destinations[a].pop(i))
            self.anthropods.append(anthropod)

        self.initialLocations = [None] * len(self.nodes)
        for a in self.anthropods:
            self.initialLocations[a.start.index] = a

        for node in self.nodes:
            node.initializeEdges()
        for node in self.nodes:
            node.analyzeGraph()
        for anthropod in self.anthropods:
            anthropod.initializeMoves(self.initialLocations)

    def __repr__(self) -> str:
        return '[Game]'

    def dump(self, anthropodLocations: list = None):
        anthropodLocations = anthropodLocations or self.initialLocations
        state = list('.' if a is None else a.name for a in anthropodLocations)

        print(''.join(state[:11]))
        print(f"  {' '.join(state[11:15])}")
        print(f"  {' '.join(state[15:19])}")

    def makeMove(self, anthropodLocations: list):
        pass

    def play(self):
        self.makeMove(self.anthropods)


game = Game('BCBDADCA')
game.dump()

print('done')
