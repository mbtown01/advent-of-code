import numpy as np


with open('2021/day2.txt') as reader:
    count, depth, horizontal = 0, 0, 0
    for cmd, units in list(a.split(' ') for a in reader.readlines()):
        units = int(units)
        count += 1
        if cmd == 'forward':
            horizontal += units
        elif cmd == 'down':
            depth += units
        elif cmd == 'up':
            depth -= units
        else:
            raise RuntimeError(f"Unexpected cmd '{cmd}'")

    result = horizontal * depth
    print(f"part 1: horizontal={horizontal}, depth={depth}, result={result}")


with open('2021/day2.txt') as reader:
    aim, count, depth, horizontal = 0, 0, 0, 0
    for cmd, units in list(a.split(' ') for a in reader.readlines()):
        units = int(units)
        count += 1
        if cmd == 'forward':
            horizontal += units
            depth += aim * units
        elif cmd == 'down':
            aim += units
        elif cmd == 'up':
            aim -= units
        else:
            raise RuntimeError(f"Unexpected cmd '{cmd}'")

    result = horizontal * depth
    print(f"part 2: horizontal={horizontal}, depth={depth}, result={result}")
