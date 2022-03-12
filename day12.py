

class Node:

    def __init__(self, name: str):
        self.name = name
        self.adjacentNodes = set()
        self.isBig = name.upper() == name
        self.isLittle = not self.isBig and name not in ['start', 'end']
        self.visitCount = 0

    def __repr__(self) -> str:
        return self.name

    def travel(self, path: list, part: int):
        path += [self]
        self.visitCount += 1

        for node in self.adjacentNodes:
            if node.isBig:
                node.travel(list(path), part)
            elif node not in path:
                node.travel(list(path), part)
            elif 2 == part:
                littleNodeVisits = list(
                    a.visitCount for a in path if a.isLittle)
                if len(littleNodeVisits) == 0 or max(littleNodeVisits) <= 1:
                    node.travel(list(path), part)

        self.visitCount -= 1


class Start(Node):

    def __init__(self):
        super().__init__('start')

    def travel(self, path: list, part: int):
        if len(path) == 0:
            return super().travel(path, part)


class End(Node):

    def __init__(self):
        super().__init__('end')
        self.allPaths = list()

    def travel(self, path: list, part: int):
        pathStr = ','.join(list(a.name for a in path+[self]))
        self.allPaths.append(pathStr)


graphMap = dict(start=Start(), end=End())
with open('day12.txt') as reader:
    for line in reader.readlines():
        nodeList = list()
        for name in line.strip().split('-'):
            node = graphMap.get(name)
            if node is None:
                node = graphMap[name] = Node(name)
            nodeList.append(node)
        nodeList[0].adjacentNodes.add(nodeList[1])
        if nodeList[0].name != 'start':
            nodeList[1].adjacentNodes.add(nodeList[0])

end = graphMap['end']
graphMap['start'].travel(list(), 1)
print(f"part 1: {len(end.allPaths)}")

end.allPaths.clear()
graphMap['start'].travel(list(), 2)
print(f"part 2: {len(end.allPaths)}")

exit(0)
