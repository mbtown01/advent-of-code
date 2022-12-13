

with open('2022/day10.txt') as reader:
    instructions = list((a.strip()) for a in reader.readlines())

cycle, regX, cycleRegXValueMap = 1, 1, {0: 1}
for instruction in instructions:
    cycleRegXValueMap[cycle] = regX
    if instruction.startswith('noop'):
        cycle += 1
    elif instruction.startswith('addx'):
        cycleRegXValueMap[cycle+1] = regX
        regX += int(instruction.split(' ')[1])
        cycleRegXValueMap[cycle+2] = regX
        cycle += 2
    else:
        raise RuntimeError(f"Unknown instruction '{instruction}'")

cycles = [20, 60, 100, 140, 180, 220]
print(f"part 1: {sum(a*cycleRegXValueMap[a] for a in cycles)}")

display = list(['.']*40 for _ in range(6))
for p in range(240):
    (row, col), regX = divmod(p, 40), cycleRegXValueMap[p+1]
    if (regX-1) <= (col) and (col) <= (regX+1):
        display[row][col] = '#'

for row in display:
    print(''.join(row))
