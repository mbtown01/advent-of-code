
class RuntimeContext:

    def __init__(self):
        self.pc = 0
        self.order = 0
        self.instructions = list()
        self.accumulator = 0
        self.atEnd = False


class Instruction:

    def __init__(self, name: str, arg: int):
        self.name = name
        self.arg = arg
        self.order = None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        order = f" | {self.order:-4d}" if self.order is not None else ""
        return f"{self.name} {self.arg:-5d}{order}"

    def reset(self):
        self.order = None

    def exec(self, runtimeContext: RuntimeContext):
        self.order = runtimeContext.order

        if self.name == 'nop':
            runtimeContext.pc += 1
        elif self.name == 'jmp':
            runtimeContext.pc += self.arg
        elif self.name == 'acc':
            runtimeContext.accumulator += self.arg
            runtimeContext.pc += 1
        else:
            raise RuntimeError(f"Instruction '{self.name}' not recognized")


class Program:

    def __init__(self, allLines: list) -> None:
        self.instructions = list()
        for line in allLines:
            instName, arg = line.split(' ')
            self.instructions.append(Instruction(instName, int(arg)))

    def _exec(self):
        for instruction in self.instructions:
            instruction.reset()

        runtimeContext = RuntimeContext()
        while(runtimeContext.pc < len(self.instructions)):
            instruction = self.instructions[runtimeContext.pc]
            if instruction.order is not None:
                return runtimeContext
            instruction.exec(runtimeContext)
            runtimeContext.order += 1

        runtimeContext.atEnd = True
        return runtimeContext

    def part1(self):
        runtimeContext = self._exec()
        print(f"part 1: {runtimeContext.accumulator}")

    def part2(self):
        swapMap = {'nop': 'jmp', 'jmp': 'nop'}
        for instruction in self.instructions:
            if instruction.name in swapMap:
                instruction.name = swapMap[instruction.name]
                runtimeContext = self._exec()
                instruction.name = swapMap[instruction.name]
                if runtimeContext.atEnd:
                    print(f"part 2: {runtimeContext.accumulator}")
                    return

        raise RuntimeError("Never found it")

    def dump(self):
        for i, instruction in enumerate(self.instructions):
            print(f"[{i:-4d}] -> {instruction}")


with open('2020/day8.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

program = Program(allLines)
program.part1()
program.part2()
