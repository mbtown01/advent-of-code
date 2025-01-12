import unittest
from os import path
from collections import defaultdict
from itertools import combinations

wireOpMap = dict(AND=lambda w1, w2: w1 & w2,
                 OR=lambda w1, w2: w1 | w2,
                 XOR=lambda w1, w2: w1 ^ w2)


class Implementation:

    class CycleDetectedError(RuntimeError):
        pass

    class Wire:

        def __init__(self):
            self.name = None
            self.opName = None
            self.value = None
            self.inputList = list()

        def __repr__(self):
            if self.opName is not None:
                w1, w2 = self.inputList[0], self.inputList[1]
                return (f"[Wire name={self.name} {w1.name} "
                        f"{self.opName} {w2.name}]")
            return f"[Wire name={self.name} value={self.value}]"

        def findAssociatedInput(self):
            if str(self.name)[0] in 'xy':
                return int(str(self.name)[1:])
            return max([a.findAssociatedInput() for a in self.inputList])

        def reset(self):
            if self.opName is not None:
                self.value = None

        def swap(self, other):
            self.name, other.name = other.name, self.name
            self.opName, other.opName = other.opName, self.opName
            self.value, other.value = other.value, self.value
            self.inputList, other.inputList = other.inputList, self.inputList

        def eval(self, *, hist: list = None):
            hist = hist or list()
            if self in hist:
                raise Implementation.CycleDetectedError()
            if self.value is None:
                inputValueList = list(a.eval(hist=hist+[self])
                                      for a in self.inputList)
                self.value = wireOpMap[self.opName](*inputValueList)
            return self.value

    def __init__(self, dataPath: str):
        self.wireMap = defaultdict(Implementation.Wire)

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                if ':' in line:
                    name, value = line.strip().split(': ')
                    self.wireMap[name].value = int(value)
                elif '->' in line:
                    eqn, name = line.strip().split(' -> ')
                    w1Name, opName, w2Name = eqn.split(' ')
                    self.wireMap[name].opName = opName
                    for n in (w1Name, w2Name):
                        self.wireMap[name].inputList.append(self.wireMap[n])

            for name, wire in self.wireMap.items():
                wire.name = name

            self.xWires = sorted(list(
                a for a in self.wireMap.values() if a.name.startswith('x')),
                key=lambda a: a.name)
            self.yWires = sorted(list(
                a for a in self.wireMap.values() if a.name.startswith('y')),
                key=lambda a: a.name)
            self.zWires = sorted(list(
                a for a in self.wireMap.values() if a.name.startswith('z')),
                key=lambda a: a.name)

    def findUnexpectedlySetBits(self, bit: int, x: int, y: int,
                                badBitCounts: list, expectedSetBit: int):
        for wire in self.wireMap.values():
            wire.reset()
        for i, (xWire, yWire) in enumerate(zip(self.xWires, self.yWires)):
            xWire.value = x if bit == i else 0
            yWire.value = y if bit == i else 0
        for i, zWire in enumerate(self.zWires):
            if (zWire.eval() == 1) != (i == expectedSetBit):
                badBitCounts[i] += 1

    def buildBadBitList(self):
        badBitCounts = [0] * len(self.xWires)
        for i in range(len(self.xWires)):
            self.findUnexpectedlySetBits(i, 0, 0, badBitCounts, -1)
            self.findUnexpectedlySetBits(i, 1, 0, badBitCounts, i)
            self.findUnexpectedlySetBits(i, 0, 1, badBitCounts, i)
            self.findUnexpectedlySetBits(i, 1, 1, badBitCounts, i+1)
        return list(a for a, b in enumerate(badBitCounts) if b > 0)

    def part1(self):
        bits = list(wire.eval() for wire in self.zWires)
        return int(''.join(str(a) for a in bits[::-1]), 2)

    def part2(self):
        # https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Full-adder_logic_diagram.svg

        inputGateListMap = defaultdict(list)
        for wire in self.wireMap.values():
            if wire.opName is not None:
                inputGateListMap[wire.findAssociatedInput()].append(wire)

        currBadBitList = self.buildBadBitList()
        gateList = list(b for a in currBadBitList for b in inputGateListMap[a])
        gateComboList = list(combinations(gateList, 2))
        finalWireList = list()
        while len(gateComboList) > 0:
            w1, w2 = gateComboList.pop(-1)
            w1.swap(w2)
            try:
                # It JUST SO HAPPENS that a swap is always between bit areas,
                # so ONLY when you remove TWO bad bits should you accept the
                # swap and continue
                nextBadBitList = self.buildBadBitList()
                if len(currBadBitList) - len(nextBadBitList) == 2:
                    finalWireList += [w1, w2]
                    currBadBitList = nextBadBitList
                    gateList = list(b for a in currBadBitList
                                    for b in inputGateListMap[a])
                    gateComboList = list(combinations(gateList, 2))
                else:
                    w1.swap(w2)
            except Implementation.CycleDetectedError:
                w1.swap(w2)

        return ','.join(sorted(list(a.name for a in finalWireList)))


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 2024)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 55920211035878)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 'btb,cmv,mwp,rdg,rmj,z17,z23,z30')


if __name__ == '__main__':
    TestCase().test_part2_real()
