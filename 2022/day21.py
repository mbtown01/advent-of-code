

class ConstNode:

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"[ConstNode {self.name} value={self.value}]"

    def eval(self):
        return self.value

    def findNode(self, name: str):
        return self if self.name == name else None


class EquationNode:

    OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    }

    def __init__(self, name: str, desc: str):
        self.name = name
        self.lvalue = None
        self.rvalue = None
        self.operator = None
        self.desc = desc

    def __repr__(self) -> str:
        return f"[EquationNode {self.name} '{self.desc}']"

    def setup(self, lvalue, operator: str, rvalue):
        self.lvalue = lvalue
        self.operator = self.OPERATORS[operator]
        self.rvalue = rvalue

    def eval(self):
        a, b = self.lvalue.eval(), self.rvalue.eval()
        return self.operator(a, b)

    def findNode(self, name: str):
        node = self.lvalue.findNode(name)
        if node is not None:
            return node

        return self.rvalue.findNode(name)


def binarySearch(leftValue: int, rightValue: int):
    humnNode = nodeMap['humn']
    rootNodeLeaves = (rootNode.lvalue, rootNode.rvalue)
    rootNodeLeavesHumn = list(a.findNode('humn') for a in rootNodeLeaves)
    constTree, varTree = \
        rootNodeLeaves if rootNodeLeavesHumn[0] is None else rootNodeLeaves[::-1]
    constValue = constTree.eval()

    while True:
        humnNode.value = leftValue
        leftEval = varTree.eval() - constValue
        humnNode.value = rightValue
        rightEval = varTree.eval() - constValue
        humnNode.value = (leftValue + rightValue) // 2
        midEval = varTree.eval() - constValue
        if leftEval < 0 and midEval > 0:
            leftValue, rightValue = leftValue, humnNode.value
        elif midEval < 0 and rightEval > 0:
            leftValue, rightValue = humnNode.value, rightValue
        elif midEval == 0:
            return humnNode.value


equationNodes, nodeMap = list(), dict()
with open('2022/day21.txt') as reader:
    for line in reader.readlines():
        name, desc = line.strip().split(': ')
        parts = desc.split(' ')
        if len(parts) == 1:
            node = ConstNode(name, int(parts[0]))
        else:
            node = EquationNode(name, desc)
            equationNodes.append(node)
        nodeMap[name] = node
    for equationNode in equationNodes:
        lvalue, operator, rvalue = equationNode.desc.split(' ')
        equationNode.setup(nodeMap[lvalue], operator, nodeMap[rvalue])


rootNode = nodeMap['root']
print(f"part 1: {rootNode.eval()}")

# I got these values by evaluating the tree and finding two spots where
# one was > 0 and one was < 0.  Could probably automate this, but...
leftValue, rightValue = 4000000000000, 3000000000000
print(f"part 2: {binarySearch(leftValue, rightValue)}")
