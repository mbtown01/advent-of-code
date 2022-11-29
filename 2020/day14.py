from itertools import permutations

with open('2020/day14.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

orMaskValue, andMaskValue = 0, 2 ^ 36 - 1
memory = dict()
for line in allLines:
    lvalue, rvalue = line.strip().split(' = ')
    if lvalue == 'mask':
        orMaskValue = int(rvalue.replace('X', '0'), 2)
        andMaskValue = int(rvalue.replace('X', '1'), 2)
    else:
        addr = int(lvalue.split('[')[1][:-1])
        memory[addr] = (int(rvalue) & andMaskValue) | orMaskValue


print(f"part 1: {sum(memory.values())}")


orMaskValue, andMaskValue = 0, 2 ^ 36 - 1
maskFloatingPermutations = [0]
memory = dict()
for line in allLines:
    lvalue, rvalue = line.strip().split(' = ')
    if lvalue == 'mask':
        orMaskValue = int(rvalue.replace('X', '0'), 2)
        andMaskValue = int(rvalue.replace('0', '1').replace('X', '0'), 2)
        floatingOffsets = list(
            2**(35 - a) for a, l in enumerate(rvalue) if l == 'X')
        maskFloatingPermutations = [0]
        for i in range(1, 2**len(floatingOffsets)):
            value = sum(floatingOffsets[j] if (i & 2**j) else 0
                        for j in range(len(floatingOffsets)))
            maskFloatingPermutations.append(value)
    else:
        addr = (int(lvalue.split('[')[1][:-1]) | orMaskValue) & andMaskValue
        for i in maskFloatingPermutations:
            memory[addr+i] = int(rvalue)


print(f"part 2: {sum(memory.values())}")
