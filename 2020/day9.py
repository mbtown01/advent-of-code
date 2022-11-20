from collections import defaultdict


def findInvalid(numbers: list, preambleLen: int):
    allPairs = defaultdict(int)
    rollingPairs = list()
    for i in range(1, preambleLen):
        rollingPairs.append(list())
        for j in range(i):
            value = numbers[i] + numbers[j]
            rollingPairs[-1].append(value)
            allPairs[value] += 1

    for i in range(preambleLen, len(numbers)):
        if allPairs[numbers[i]] == 0:
            return numbers[i]

        for row in rollingPairs:
            allPairs[row.pop(0)] -= 1
        latestRollingPairs = list(
            numbers[i] + numbers[i+j] for j in range(-preambleLen+1, 0))
        rollingPairs = rollingPairs[1:]
        rollingPairs.append(latestRollingPairs)
        for value in latestRollingPairs:
            allPairs[value] += 1
        for key, value in list(allPairs.items()):
            if value == 0:
                del allPairs[key]


def findWeakness(numbers: list, value: int):
    for i in range(len(numbers)):
        total = numbers[i]
        for j in range(i+1, len(numbers)):
            total += numbers[j]
            if total == value:
                weakValues = numbers[i:j+1]
                minValue = min(weakValues)
                maxValue = max(weakValues)
                return minValue + maxValue
            if total > value:
                break

    raise RuntimeError(f"Value {value} never found")


with open('2020/day9.txt') as reader:
    numbers = list(int(a.strip()) for a in reader.readlines())

value = findInvalid(numbers, 25)

print(f"part 1: value={value}")

weakness = findWeakness(numbers, value)

print(f"part 2: {weakness}")
