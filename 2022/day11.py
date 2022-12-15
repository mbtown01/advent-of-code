
class MonkeyPt1:
    def __init__(self, id: int):
        self.id = id
        self.items = list()
        self.operations = list()
        self.testDivisibleBy = None
        self.monkeyIfTrue = None
        self.monkeyIfFalse = None
        self.inspectionCount = 0

    def setItems(self, items: list):
        self.items = items

    def scaleWorry(self, worryLevel: int):
        return worryLevel // 3

    def exec(self, monkeyList: list):
        while len(self.items):
            item = self.items.pop(0)
            a, op, b = self.operations
            a, b = a or item, b or item
            worryLevel = (a + b) if op == '+' else (a * b)
            worryLevel = self.scaleWorry(worryLevel)

            result = worryLevel % self.testDivisibleBy
            nextMonkeyId = \
                self.monkeyIfFalse if result > 0 else self.monkeyIfTrue
            monkeyList[nextMonkeyId].items.append(worryLevel)
            self.inspectionCount += 1


class MonkeyPt2(MonkeyPt1):

    def __init__(self, id: int):
        self.worryModulo = 1
        super().__init__(id)

    def scaleWorry(self, worryLevel: int):
        return worryLevel % self.worryModulo

    def exec(self, monkeyList: list):
        if self.worryModulo == 1:
            for monkey in monkeyList:
                self.worryModulo *= monkey.testDivisibleBy
        return super().exec(monkeyList)


def exec(monkeyType: type, itemType: type, rounds: int):

    with open('2022/day11.txt') as reader:
        monkeyList = list()
        for line in (a.strip() for a in reader.readlines()):
            parts = line.split(' ')
            if line.startswith('Monkey'):
                monkeyList.append(monkeyType(int(parts[1][:-1])))
            elif line.startswith('Starting items'):
                monkeyList[-1].setItems(list(
                    itemType(a) for a in line.split(':')[1].split(', ')))
            elif line.startswith('Test'):
                if parts[1] != 'divisible':
                    raise RuntimeError("Has to be 'divisible' by")
                monkeyList[-1].testDivisibleBy = int(parts[3])
            elif line.startswith('Operation:'):
                monkeyList[-1].operations = list(
                    None if a == 'old' else a
                    for a in line.split(' = ')[1].split(' '))
                for i in [0, 2]:
                    if monkeyList[-1].operations[i] is not None:
                        monkeyList[-1].operations[i] = \
                            itemType(monkeyList[-1].operations[i])
                if monkeyList[-1].operations[1] not in ['+', '*']:
                    raise RuntimeError(f"invalid operation '{line}'")
            elif line.startswith('If true:'):
                monkeyList[-1].monkeyIfTrue = int(parts[5])
            elif line.startswith('If false:'):
                monkeyList[-1].monkeyIfFalse = int(parts[5])
            elif line != '':
                raise RuntimeError(f"bad line '{line}'")

    for _ in range(rounds):
        for monkey in monkeyList:
            monkey.exec(monkeyList)

    inspectionCounts = sorted(list(a.inspectionCount for a in monkeyList))
    return inspectionCounts[-1]*inspectionCounts[-2]


print(f"part 1: {exec(MonkeyPt1, int, 20)}")
print(f"part 2: {exec(MonkeyPt2, int, 10000)}")
