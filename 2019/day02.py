import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.program = list(
                int(a) for a in reader.readline().strip().split(','))

    @classmethod
    def exec(cls, program: list):
        pc = 0
        while pc < len(program) and program[pc] != 99:
            if program[pc] == 1:
                lhs, rhs, dest = program[pc+1:pc+4]
                program[dest] = program[lhs] + program[rhs]
                pc += 4
            elif program[pc] == 2:
                lhs, rhs, dest = program[pc+1:pc+4]
                program[dest] = program[lhs] * program[rhs]
                pc += 4
            else:
                raise RuntimeError(f"Unknown opcode {program[pc]}")
        return tuple(program)

    def execMutate(self, value: int):
        program = self.program.copy()
        program[1], program[2] = value // 100, value % 100
        return self.exec(program)[0]

    def part1(self):
        return self.execMutate(1202)

    def part2(self):
        vLow, vHigh, value = 0, 9999, 5000
        expected, result = 19690720, self.execMutate(value)
        while result != expected:
            if result > expected:
                vHigh, value = value, (vLow + value) // 2
            else:
                vLow, value = value, (value + vHigh) // 2
            result = self.execMutate(value)
        return value


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        self.assertEqual(Implementation.exec(
            [1, 0, 0, 0, 99]), (2, 0, 0, 0, 99))
        self.assertEqual(Implementation.exec(
            [2, 3, 0, 3, 99]), (2, 3, 0, 6, 99))
        self.assertEqual(Implementation.exec(
            [2, 4, 4, 5, 99, 0]), (2, 4, 4, 5, 99, 9801))
        self.assertEqual(Implementation.exec(
            [1, 1, 1, 4, 99, 5, 6, 0, 99]), (30, 1, 1, 4, 2, 5, 6, 0, 99))

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 4090701)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 6421)
