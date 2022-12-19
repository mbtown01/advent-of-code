

from functools import total_ordering


def parseList(line: str):
    result, index = list(), 1
    if line[0] != '[':
        raise RuntimeError('parse error')

    while line[index] != ']':
        if line[index] == ',':
            index += 1
        elif line[index] >= '0' and line[index] <= '9':
            start, index = index, index + 1
            while line[index] >= '0' and line[index] <= '9':
                index += 1
            result.append(int(line[start:index]))
        elif line[index] == '[':
            subResult, subOffset = parseList(line[index:])
            result.append(subResult)
            index += subOffset
        else:
            raise RuntimeError('parse error')

    return result, index+1


def compareLists(leftArray, rightArray):
    index = 0
    while index < len(leftArray) and index < len(rightArray):
        left, right = leftArray[index], rightArray[index]
        if type(left) == int and type(right) == int:
            if left != right:
                return left < right
        else:
            left = [left] if type(left) == int else left
            right = [right] if type(right) == int else right
            result = compareLists(left, right)
            if type(result) == bool:
                return result

        index += 1

    if len(leftArray) != len(rightArray):
        return len(leftArray) < len(rightArray)


with open('2022/day13.txt') as reader:
    lines = list(a.strip() for a in reader.readlines())
    lines = list(a for a in lines if len(a) > 0)

total = 0
for i in range(0, len(lines), 2):
    leftArray = parseList(lines[i])[0]
    rightArray = parseList(lines[i+1])[0]
    result = compareLists(leftArray, rightArray)
    if result:
        total += i//2 + 1
print(f"part 1: {total}")


@total_ordering
class PacketContainer:

    def __init__(self, line: str) -> None:
        self.line = line
        self.packet = parseList(line)[0]

    def __le__(self, other: object) -> bool:
        result = compareLists(self.packet, other.packet)
        result = True if result is None else result
        return result

    def __eq__(self, other: object) -> bool:
        result = compareLists(self.packet, other.packet)
        return result is None


final = sorted(list(PacketContainer(a) for a in lines + ['[[2]]', '[[6]]']))
prod = (list(a.line for a in final).index('[[2]]') + 1) * \
    (list(a.line for a in final).index('[[6]]') + 1)
print(f"part 2: {prod}")
