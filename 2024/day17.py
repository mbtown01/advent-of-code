import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.registerValues = dict()
            for line in reader.readlines():
                if line.startswith('Register'):
                    reg, val = line.strip().split(': ')
                    self.registerValues[reg[-1]] = int(val)
                if line.startswith('Program'):
                    self.program = list(
                        int(a) for a in line.strip().split(': ')[1].split(','))

    def part1(self):
        outList, program, pc = list(), self.program.copy(), 0
        regs = self.registerValues.copy()
        comboRegVals = {4: 'A', 5: 'B', 6: 'C'}
        advRegMap = {0: 'A', 6: 'B', 7: 'C'}

        def combo(v: int):
            return v if v < 4 else regs[comboRegVals[v]]

        while pc < len(program):
            opCode, operand = program[pc], program[pc+1]
            # ADV, BDV, CDV
            if opCode in (0, 6, 7):
                regs[advRegMap[opCode]] = regs['A'] // 2 ** combo(operand)
            # BXL, BXC
            elif opCode in (1, 4):
                regs['B'] = regs['B'] ^ (operand if opCode == 1 else regs['C'])
            # BST
            elif opCode == 2:
                regs['B'] = combo(operand) % 8
            # JNZ
            elif opCode == 3:
                pc = (pc + 2) if regs['A'] == 0 else operand
            # OUT
            elif opCode == 5:
                outList.append(combo(operand) % 8)
            if opCode != 3:
                pc += 2

        return ','.join(str(a) for a in outList)

    def part2(self):
        def findSolution(index: int, result: int):
            if index < 0:
                return result

            rtn = None
            for i in range(8):
                regA = result*8 + i
                regB = (regA % 8) ^ 1
                regC = regA // 2 ** regB
                regB = regA ^ 4 ^ regC
                if regB % 8 == self.program[index]:
                    rtn = findSolution(index-1, regA)
                    if rtn is not None:
                        break

            return rtn

        return findSolution(len(self.program)-1, 0)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, '4,6,3,5,6,3,5,2,1,0')

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, '7,6,1,5,3,1,4,2,6')

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 164541017976509)
