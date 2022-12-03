

def play(numbers: list, maxTurn: int):
    numberTurnMap = {number: [turn] for turn, number in enumerate(numbers)}
    lastSpokenNumber = numbers[-1]
    for turn in range(len(numbers), maxTurn):
        lastSpokenOnTurns = numberTurnMap.get(lastSpokenNumber, [])
        if len(lastSpokenOnTurns) < 2:
            lastSpokenNumber = 0
        else:
            lastSpokenNumber = lastSpokenOnTurns[0] - lastSpokenOnTurns[1]

        lastSpokenOnTurns = numberTurnMap.get(lastSpokenNumber, [])
        lastSpokenOnTurns.insert(0, turn)
        if len(lastSpokenOnTurns) > 2:
            lastSpokenOnTurns.pop()
        numberTurnMap[lastSpokenNumber] = lastSpokenOnTurns

    return lastSpokenNumber


with open('2020/day15.txt') as reader:
    numbers = list(int(a) for a in reader.readline().strip().split(','))

print(f"part 1: {play(numbers, 2020)}")
print(f"part 2: {play(numbers, 30000000)}")
