from collections import defaultdict
from enum import Enum
from itertools import permutations


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
                    nodePaths[node] = thisPath[1:]
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

    def __init__(self, name: str, location: Node, destination: Node):
        self.name = name
        self.start = location
        self.destination = destination

    def __repr__(self) -> str:
        return (f"[Anthropod '{self.name}']")

    def locationIsFinal(self, location: Node, anthropodLocations: list):
        if location != self.destination:
            return False

        southernEdgeList = list(
            a for a in location.edges if a.direction == Edge.Direction.SOUTH)
        if len(southernEdgeList) == 0:
            return True

        southernNode = southernEdgeList[0].destination
        southernAnthropod = anthropodLocations[southernNode.index]
        return southernAnthropod.locationIsFinal(
            southernNode, anthropodLocations)

    def getAvailableMoves(self, nodes: list, anthropodLocations: list):
        location = nodes[anthropodLocations.index(self)]
        if self.locationIsFinal(location, anthropodLocations):
            return None

        pathList = list(b for a, b in location.nodePaths.items()
                        if location.isBurrow != a.isBurrow)
        if location.isBurrow and location != self.destination:
            pathList.append(location.nodePaths[self.destination])

        moveInfoList = list(
            (a, len(a) * self.ENERGY_MAP[self.name]) for a in pathList)
        moveInfoList = sorted(moveInfoList, key=lambda a: a[1])

        availableMoveInfo = list()
        for path, energy in moveInfoList:
            if all(anthropodLocations[a.index] is None for a in path):
                availableMoveInfo.append((path, energy))
        return availableMoveInfo


class Game:

    class Result:
        def __init__(self, sequence: list, energy: int):
            self.sequence = sequence
            self.energy = energy

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

        for node in self.nodes:
            node.initializeEdges()
        for node in self.nodes:
            node.analyzeGraph()

    def __repr__(self) -> str:
        return '[Game]'

    def _dump(self, anthropodLocations: list = None):
        state = list('.' if a is None else a.name for a in anthropodLocations)

        print(''.join(state[:11]))
        print(f"  {' '.join(state[11:15])}")
        print(f"  {' '.join(state[15:19])}")

    def _play(self,
              anthropods: list,
              anthropodLocations: list,
              moves: list,
              energy: int):
        if len(anthropods) == 0:
            return dict(moves=moves, energy=energy)

        anthropod = anthropods[0]
        moveInfo = anthropod.getAvailableMoves(
            self.nodes, anthropodLocations)
        for movePath, moveEnergy in moveInfo:
            newLocations = anthropodLocations.copy()
            newLocations[movePath[-1].index] = anthropod
            newLocations[movePath[0].index] = None

            result = self._play(
                anthropods[1:], newLocations, moves + [(movePath, moveEnergy)])

        return None

    def play(self):
        """ There are only 8*7*6*5*4*3*2 POSSIBLE sequences of first moves.
        If we assume that a 2nd move happens as SOON as it's possible to make
        that move, then those moves essentially don't count so there are 40320
        total moves.  Strategy is to evaluate the energy used for each
        unique sequence of anthropod moves and find the lowest energy
        """
        anthropodLocations = [None] * len(self.nodes)
        for a in self.anthropods:
            anthropodLocations[a.start.index] = a

        for anthropodSequence in permutations(self.anthropods):
            best = self._play(anthropodSequence, anthropodLocations, list(), 0)

        # self._dump(anthropodLocations)
        # return self._play(self.anthropods, anthropodLocations)
        return None


game = Game('BCBDADCA')
game.play()

print('done')


"""
https://csacademy.com/app/graph_editor/
#################
#..  .  .  .  ..#
###B1#C1#B2#D1###
  #A2#D2#C2#A1#
  #############

A1: [D1, B1]
A2: None
B1: [C1, D2]
B2: [C1, D2]
C1: [B2]
C2: None
D1: [A1]
D2: [C1, D1, A1]

A1 D1
A1 B1
B1 C1
B1 D2
B2 C1
B2 D2
C1 B2
D1 A1
D2 C1
D2 D1
D2 A1
"""
