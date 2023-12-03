from collections import defaultdict

adjacencies = list((a, b) for b in range(-1, 2) for a in range(-1, 2))
adjacencies = list(a for a in adjacencies if a != (0, 0))
numbers = list(chr(ord('0')+a) for a in range(10))
numbersAndBlanks = numbers + ['.']

part1Sum, part2Sum = 0, 0
with open('2023/day3.txt', encoding="utf8") as reader:
    schematic = list(line.strip() for line in reader)
    gearNumbersMap = defaultdict(set)

    for y, row in enumerate(schematic):
        numberStarts, numberEnds = [], []
        for x, c in enumerate(row):
            if c in numbers and (x == 0 or row[x-1] not in numbers):
                numberStarts.append(x)
            if c in numbers and (x == len(row)-1 or row[x+1] not in numbers):
                numberEnds.append(x)

        for start, end in zip(numberStarts, numberEnds):
            symbols = list(
                (schematic[y+dy][x+dx], x+dx, y+dy)
                for x in range(start, end+1)
                for dx, dy in adjacencies
                if (x + dx >= 0 and x + dx < len(row) and
                    y + dy >= 0 and y + dy < len(schematic) and
                    schematic[y+dy][x+dx] not in numbersAndBlanks)
            )
            if len(symbols) > 0:
                number = int(row[start:end+1])
                part1Sum += number
                for symbol, rx, ry in symbols:
                    if symbol == '*':
                        gearNumbersMap[rx, ry].add((start, y, number))

    for numberSet in gearNumbersMap.values():
        if len(numberSet) == 2:
            numberList = list(a[2] for a in numberSet)
            part2Sum += numberList[0] * numberList[1]

print(f"part 1: {part1Sum}")
print(f"part 2: {part2Sum}")
