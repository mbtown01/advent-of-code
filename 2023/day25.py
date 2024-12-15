from collections import defaultdict
import unittest


class Node:

    def __init__(self, name: str) -> None:
        self.name = name
        self.edgeList = list()

    def __repr__(self) -> str:
        return f"[Node name='{self.name}' edges={len(self.edgeList)}]"


class Implementation:

    def __init__(self, dataPath: str):
        self.nodeMap = dict()

        def getNode(name: str):
            node = self.nodeMap.get(name)
            if node is None:
                node = self.nodeMap[name] = Node(name)
            return node

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                sourceName, destNameText = line.strip().split(": ")
                sourceNode = getNode(sourceName)
                for destName in destNameText.split(" "):
                    destNode = getNode(destName)
                    sourceNode.edgeList.append(destNode)
                    destNode.edgeList.append(sourceNode)

    def findCycle(self, node: Node, seenNodes: list, level: int):
        if level == 0:
            return None

        seenNodes = seenNodes + [node]
        for nextNode in node.edgeList:
            if nextNode == seenNodes[0] and len(seenNodes) > 4:
                return seenNodes
            if nextNode not in seenNodes:
                result = self.findCycle(nextNode, seenNodes, level-1)
                if result is not None:
                    return result

        return None

    def part1(self):
        nodeCycleCountMap = defaultdict(int)
        # TODO: Analyze this by edge not node
        for node in self.nodeMap.values():
            cycle = self.findCycle(node, list(), 8)
            if cycle is None:
                raise RuntimeError(f"{node.name}: NO CYCLE")
            # print(f"{node.name}: {len(cycle)} {', '.join(a.name for a in cycle)}")
            for n0, n1 in zip(cycle[:-1], cycle[1:]):
                edge = (n0, n1) if n0.name < n1.name else (n1, n0)
                nodeCycleCountMap[edge] += 1

        return 0

    def part2(self):
        return 0


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 21)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 10033566)

    # def test_part2_ex(self):
    #     impl = Implementation(f'2023/data/{__name__}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 1030)

    # def test_part2_real(self):
    #     impl = Implementation(f'2023/data/{__name__}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 560822911938)
