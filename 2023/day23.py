import unittest


class Node:

    def __init__(self, loc: tuple, typeChar: str):
        self.loc = loc
        self.typeChar = typeChar
        self.edgeStepMap = dict()
        self.name = f"node_{loc[0]:03d}_{loc[1]:03d}"

    def __repr__(self) -> str:
        return f"[Node ({self.loc}) '{self.typeChar}']"

    def isTwoWaySymmetric(self):
        return len(self.edgeStepMap) == 2 and \
            all(self in a.edgeStepMap for a in self.edgeStepMap)

    def canRerouteAround(self, honorSlope: bool):
        if honorSlope:
            nodeList = list(self.edgeStepMap.keys()) + [self]
            return len(nodeList) == 3 and \
                all(a.isTwoWaySymmetric() for a in nodeList)
        else:
            return self.isTwoWaySymmetric()

    def rerouteAround(self):
        for n1 in list(self.edgeStepMap.keys()):
            for n2 in list(a for a in self.edgeStepMap if a != n1):
                n1.edgeStepMap[n2] = \
                    n1.edgeStepMap.pop(self) + self.edgeStepMap.pop(n2)

    def findLongestPath(self, path: list, finalNode, steps: int):
        if self == finalNode:
            return steps

        localPath = path + [self]
        return max(list(
            a.findLongestPath(localPath, finalNode, steps+stepCount)
            for a, stepCount in self.edgeStepMap.items()
            if a not in localPath
        ) + [0])


class Implementation:
    allTypeChars = '.><^v'

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.nodeMap = {(j, i): Node((j, i), typeChar)
                            for j, row in enumerate(reader)
                            for i, typeChar in enumerate(row)
                            if typeChar in self.allTypeChars}

        nodeList = list(self.nodeMap.items())
        nodeList.sort(key=lambda a: a[0])
        self.startNode = nodeList[0][1]
        self.endNode = nodeList[-1][1]

    def initNetwork(self, *, honorSlope: bool = True):
        nextLocCharTypeMap = {
            (0, -1): '.<' if honorSlope else self.allTypeChars,
            (0, 1): '.>' if honorSlope else self.allTypeChars,
            (-1, 0): '.^' if honorSlope else self.allTypeChars,
            (1, 0): '.v' if honorSlope else self.allTypeChars,
        }

        # First populate each node's nodeList with the potential paths out
        for loc, node in self.nodeMap.items():
            for delta, charList in nextLocCharTypeMap.items():
                nextLoc = tuple(loc[a] + delta[a] for a in range(2))
                nextNode = self.nodeMap.get(nextLoc)
                if nextNode is not None and nextNode.typeChar in charList:
                    node.edgeStepMap[nextNode] = 1

        # Then simplify the graph by identifying any nodes that can be
        # removed and their incoming/outgoing edges be re-routed to
        # simplify the network (straight paths in the maze)
        for node in self.nodeMap.values():
            if node.canRerouteAround(honorSlope):
                node.rerouteAround()

    def emitGraph(self, path: str):
        # checkout https://edotor.net/
        with open(path, "w", encoding="utf8") as file:
            print("digraph {", file=file)
            for node in self.nodeMap.values():
                for nextNode, steps in node.edgeStepMap.items():
                    path = f"{node.name} -> {nextNode.name}"
                    print(f"    {path} [label={steps}];", file=file)

            startName, endName = self.startNode.name, self.endNode.name
            print(f"    {startName} [shape=diamond, color=green];", file=file)
            print(f"    {endName} [shape=diamond, color=red];", file=file)
            print("}", file=file)

    def part1(self):
        self.initNetwork(honorSlope=True)
        self.emitGraph('graph.txt')
        return self.startNode.findLongestPath([], self.endNode, 0)

    def part2(self):
        self.initNetwork(honorSlope=False)
        self.emitGraph('graph.txt')
        return self.startNode.findLongestPath([], self.endNode, 0)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 94)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 2310)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 154)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 6738)
