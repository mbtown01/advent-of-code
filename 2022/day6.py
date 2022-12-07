

with open('2022/day6.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())


def findStartOfPacket(line: str, windowLen: int):
    for i in range(len(line)-windowLen+1):
        if len({a: a for a in line[i:i+windowLen]}) == windowLen:
            return i + windowLen
    raise RuntimeError("never found start of packet")


print(f"part 1: {findStartOfPacket(allLines[0], 4)}")
print(f"part 1: {findStartOfPacket(allLines[0], 14)}")
