import unittest

from collections import defaultdict


class Implementation:

    def __init__(self, dataPath: str):
        adjacencies = list((a, b) for b in range(-1, 2) for a in range(-1, 2))
        adjacencies = list(a for a in adjacencies if a != (0, 0))
        numbers = list(chr(ord('0')+a) for a in range(10))

        with open(dataPath, encoding="utf8") as reader:
            schematic = list(line.strip() for line in reader)

        gearNumbersMap = defaultdict(set)
        self.part1Sum, self.part2Sum = 0, 0
        for y, row in enumerate(schematic):
            numberStarts, numberEnds = [], []
            for x, c in enumerate(row):
                if c in numbers and (x == 0 or row[x-1] not in numbers):
                    numberStarts.append(x)
                if c in numbers and (x == len(row)-1 or row[x+1] not in numbers):
                    numberEnds.append(x)

            for start, end in zip(numberStarts, numberEnds):
                adjacentSymbolList = list(
                    (schematic[y+dy][x+dx], x+dx, y+dy)
                    for x in range(start, end+1)
                    for dx, dy in adjacencies
                    if (x + dx >= 0 and x + dx < len(row) and
                        y + dy >= 0 and y + dy < len(schematic) and
                        schematic[y+dy][x+dx] not in numbers + ['.'])
                )
                if len(adjacentSymbolList) > 0:
                    number = int(row[start:end+1])
                    self.part1Sum += number
                    for symbol, rx, ry in adjacentSymbolList:
                        if symbol == '*':
                            gearNumbersMap[rx, ry].add((start, y, number))

        for numberSet in gearNumbersMap.values():
            if len(numberSet) == 2:
                numberList = list(a[2] for a in numberSet)
                self.part2Sum += numberList[0] * numberList[1]

    def part1(self):
        return self.part1Sum

    def part2(self):
        return self.part2Sum


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 4361)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 559667)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 467835)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 86841457)
