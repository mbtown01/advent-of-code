import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.program = list(
                int(a) for a in reader.readline().strip().split(','))

    @classmethod
    def exec(cls, program: list, inputQueue: list, outputqueue: list):
        pc = 0
        while pc < len(program) and program[pc] != 99:
            mode, opCode = divmod(program[pc], 100)
            if opCode == 1:
                lhs, rhs, dest = program[pc+1:pc+4]
                program[dest] = program[lhs] + program[rhs]
                pc += 4
            elif opCode == 2:
                lhs, rhs, dest = program[pc+1:pc+4]
                program[dest] = program[lhs] * program[rhs]
                pc += 4
            elif opCode == 3:
                dest = program[pc+1]
                program[dest] = inputQueue.pop()
                pc += 2
            elif opCode == 4:
                dest = program[pc+1]
                outputqueue.append(program[dest])
                pc += 2
            else:
                raise RuntimeError(f"Unknown opcode {program[pc]}")
        return tuple(program)

    def execMutate(self, value: int):
        program = self.program.copy()
        return self.exec(program)[0]

    def part1(self):
        pass

    def part2(self):
        return None


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    # def test_part1_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 9999999)

    # def test_part1_real(self):
    #     impl = Implementation(f'{self._pathPrefix}_real.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 9999999)

    # def test_part2_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 9999999)

    # def test_part2_real(self):
    #     impl = Implementation(f'{self._pathPrefix}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 9999999)
