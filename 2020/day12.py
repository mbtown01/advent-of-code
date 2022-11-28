

with open('2020/day12.txt') as reader:
    instructions = list(a.strip() for a in reader.readlines())


def resetAngle(angle: int):
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


def part1():
    cmdDxytMap = {
        'N': (0, 1, 0),
        'S': (0, -1, 0),
        'E': (1, 0, 0),
        'W': (-1, 0, 0),
        'L': (0, 0, 1),
        'R': (0, 0, -1),
    }

    dirDxytMap = {
        90: (0, 1, 0),
        270: (0, -1, 0),
        0: (1, 0, 0),
        180: (-1, 0, 0),
    }

    posXyt = [0, 0, 0]
    for instruction in instructions:
        cmd, value = instruction[0], int(instruction[1:])

        dXyt = dirDxytMap[posXyt[2]] if cmd == 'F' else cmdDxytMap[cmd]
        posXyt = list(posXyt[i] + value*dXyt[i] for i in range(len(posXyt)))
        posXyt[2] = resetAngle(posXyt[2])

    distance = abs(posXyt[0]) + abs(posXyt[1])
    print(f"part 1: {distance}")


def part2():
    cmdDxytMap = {
        'N': (0, 1),
        'S': (0, -1),
        'E': (1, 0),
        'W': (-1, 0),
        'F': (0, 0),
    }

    posXy = [0, 0]
    wayPtXy = [10, 1]
    for instruction in instructions:
        cmd, value = instruction[0], int(instruction[1:])

        if cmd in 'NEWS':
            dXyt = cmdDxytMap[cmd]
            wayPtXy = list(
                wayPtXy[i] + value*dXyt[i] for i in range(len(wayPtXy)))
        elif cmd in 'LR':
            if cmd == 'R':
                value = resetAngle(-value)
            if value == 90:
                wayPtXy = (-wayPtXy[1], wayPtXy[0])
            elif value == 180:
                wayPtXy = (-wayPtXy[0], -wayPtXy[1])
            elif value == 270:
                wayPtXy = (wayPtXy[1], -wayPtXy[0])
            else:
                raise RuntimeError(f"Invalid rotation {value}")
        elif cmd == 'F':
            for i in range(value):
                posXy = list(posXy[i] + wayPtXy[i] for i in range(len(posXy)))

    distance = abs(posXy[0]) + abs(posXy[1])
    print(f"part 2: {distance}")


part1()
part2()
