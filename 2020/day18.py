import unittest
from os import path


class Implementation:

    opMap = {'+': lambda a, b: a+b, '*': lambda a, b: a*b}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.equationList = list(a for a in reader.readlines())

    def evalEquation(self, tokenList: list, orderOps: bool):
        valStack, opStack = list(), list()
        while len(tokenList) > 0 and (t := tokenList.pop(0)) != ')':
            if t in '0123456789':
                valStack.append(int(t))
            elif t == '(':
                valStack.append(self.evalEquation(tokenList, orderOps))
            elif t in '+*':
                opStack.append(t)

            if orderOps and len(opStack) > 0:
                if len(opStack) == len(valStack)-1 and opStack[-1] == '+':
                    rVal, lVal = valStack.pop(-1), valStack.pop(-1)
                    opStack.pop(-1)
                    valStack.append(lVal+rVal)

        value = valStack[0]
        for op, rVal in zip(opStack, valStack[1:]):
            value = self.opMap[op](value, rVal)

        return value

    def part1(self):
        return sum(self.evalEquation(list(a for a in b), False)
                   for b in self.equationList)

    def part2(self):
        return sum(self.evalEquation(list(a for a in b), True)
                   for b in self.equationList)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_dummy1(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.evalEquation(list(a for a in '2+3*4+5'), False)
        self.assertEqual(result, 25)

    def test_dummy2(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.evalEquation(list(a for a in '2+3*4+5'), True)
        self.assertEqual(result, 45)

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 26335)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 21022630974613)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 693891)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 169899524778212)
