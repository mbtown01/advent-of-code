from math import ceil, floor
from functools import reduce


class KeepGoingWarning(RuntimeWarning):
    pass


class Element:

    def __init__(self, length: int) -> None:
        self.length = length
        self.parent = None


class Value(Element):

    def __init__(self, value: int) -> None:
        super().__init__(1)
        self.value = value
        self.index = None
        self.neighbors = [None, None]

    def __repr__(self) -> str:
        return str(self.value)

    def copy(self):
        return Value(self.value)

    def indexElementTree(self, valueList: list):
        self.index = len(valueList)
        if len(valueList) > 0:
            self.neighbors[0] = valueList[-1]
            self.neighbors[0].neighbors[1] = self
        valueList.append(self)

    def magnitude(self):
        return self.value

    @classmethod
    def tryParse(cls, equation: str):
        token = equation[0]
        if token >= '0' and token <= '9':
            return Value(int(token))


class Pair(Element):

    def __init__(self, lValue: Element, rValue: Element) -> None:
        super().__init__(3+lValue.length+rValue.length)
        self.elements = [lValue, rValue]
        for element in self.elements:
            element.parent = self

    def __repr__(self) -> str:
        return f"[{self.elements[0]},{self.elements[1]}]"

    def copy(self):
        return Pair(
            self.elements[0].copy(),
            self.elements[1].copy()
        )

    def indexElementTree(self, valueList: list):
        for element in self.elements:
            element.indexElementTree(valueList)

    def explode(self, fromSide: int, toSide: int):
        pair = self.elements[fromSide]
        self.elements[fromSide] = Value(0)
        for side in range(2):
            neighbor = pair.elements[side].neighbors[side]
            if neighbor is not None:
                neighbor.value += pair.elements[side].value

        raise KeepGoingWarning()

    def explodeSearch(self, level: int, valueList: list = None):
        if valueList is None:
            self.indexElementTree(list())

        if level == 4:
            if isinstance(self.elements[0], Pair):
                self.explode(0, 1)
            if isinstance(self.elements[1], Pair):
                self.explode(1, 0)

        for element in self.elements:
            if isinstance(element, Pair):
                element.explodeSearch(level+1, valueList)

    def splitSearch(self):
        for i, element in enumerate(list(self.elements)):
            if isinstance(element, Pair):
                element.splitSearch()
            if isinstance(element, Value) and element.value >= 10:
                lValue = Value(int(floor(element.value/2)))
                rValue = Value(int(ceil(element.value/2)))
                self.elements[i] = Pair(lValue, rValue)
                raise KeepGoingWarning()

    def reduce(self):
        while True:
            try:
                self.explodeSearch(1)
                self.splitSearch()
                return self
            except KeepGoingWarning:
                continue

    def magnitude(self):
        return 3*self.elements[0].magnitude() + 2*self.elements[1].magnitude()

    @classmethod
    def tryParse(cls, equation: str):
        if equation[0] == '[':
            equation = equation[1:]
            lValue = Value.tryParse(equation) or Pair.tryParse(equation)
            equation = equation[lValue.length+1:]
            rValue = Value.tryParse(equation) or Pair.tryParse(equation)
            return Pair(lValue, rValue)


testSet = [
    dict(
        input='[[[[[9,8],1],2],3],4]',
        output='[[[[0,9],2],3],4]',
    ),
    dict(
        input='[7,[6,[5,[4,[3,2]]]]]',
        output='[7,[6,[5,[7,0]]]]',
    ),
    dict(
        input='[[6,[5,[4,[3,2]]]],1]',
        output='[[6,[5,[7,0]]],3]',
    ),
    dict(
        input='[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
        output='[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
    ),
    dict(
        input='[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
        output='[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
    ),
    dict(
        input='[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]',
        output='[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
    )
]

for i, testInfo in enumerate(testSet):
    pair = Pair.tryParse(testInfo['input'])
    pair.reduce()
    result = str(pair)

    if result != testInfo['output']:
        print(f"Test {i} failed")
        print(f"    Expected '{testInfo['output']}'")
        print(f"    Received '{result}'")


with open('day18.txt') as reader:
    numberList = list(Pair.tryParse(a.strip()) for a in reader.readlines())
finalNumber = reduce(lambda a, b: Pair(a, b).copy().reduce(), numberList)
print(f"part 1: {finalNumber.magnitude()}")

maxValue = 0
for i, lValue in enumerate(numberList):
    for j, rValue in enumerate(numberList):
        if lValue != rValue:
            pair = Pair(lValue.copy(), rValue.copy())
            maxValue = max(pair.reduce().magnitude(), maxValue)

print(f"part 2: {maxValue}")
