

class ListEntry:

    def __init__(self, value: int):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self) -> str:
        return f"[ListEntry value={self.value}]"


class MixableList:

    def __init__(self, numbers: list):
        self.entryList = list(ListEntry(a) for a in numbers)
        self.entryMap = {a: b for (a, b) in enumerate(self.entryList)}
        self.zeroEntry = None
        for index, entry in enumerate(self.entryList):
            entry.prev = self.entryMap[(index - 1) % len(numbers)]
            entry.next = self.entryMap[(index + 1) % len(numbers)]
            if entry.value == 0:
                self.zeroEntry = entry

    def mix(self):
        for index in range(len(self.entryList)):
            mover, total = self.entryMap[index], len(self.entryList)
            dest, moverMod = mover, mover.value % (total - 1)
            for _ in range(moverMod):
                dest = dest.next

            if mover != dest:
                mover.prev.next, mover.next.prev = mover.next, mover.prev
                mover.prev, mover.next = dest, dest.next
                mover.prev.next, mover.next.prev = mover, mover

        prevSet = set(a.prev for a in self.entryList)
        nextSet = set(a.next for a in self.entryList)
        if len(prevSet) + len(nextSet) != 2*len(self.entryList):
            raise RuntimeError()

    def getResult(self):
        ptr, result = self.zeroEntry, 0
        for i in range(3):
            moveCount = 1000 % len(self.entryList)
            for _ in range(moveCount):
                ptr = ptr.next
            result += ptr.value
        return result


with open('2022/day20.txt') as reader:
    numbers = list(int(a.strip()) for a in reader.readlines())

mixableList = MixableList(numbers)
mixableList.mix()
print(f"part 1: {mixableList.getResult()}")

mixableList = MixableList(list(a*811589153 for a in numbers))
for _ in range(10):
    print("scanning....")
    mixableList.mix()
print(f"part 2: {mixableList.getResult()}")
