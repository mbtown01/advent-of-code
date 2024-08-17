import unittest
from collections import defaultdict


class Axis:

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"[Axis [{self.start}, {self.end})] len={len(self)}]"

    def __len__(self):
        return self.end - self.start + 1

    def contains(self, value: int):
        return self.start <= value <= self.end

    def intersect(self, other):
        if self.contains(other.start) and not self.contains(other.end):
            return Axis(other.start, self.end)
        if self.contains(other.end) and not self.contains(other.start):
            return Axis(self.start, other.end)
        if self.contains(other.start) and self.contains(other.end):
            return other
        if other.contains(self.start) and other.contains(self.end):
            return self
        return None


class Brick:

    def __init__(self, axes: list, *, name: str = 'noname') -> None:
        self.axes = axes
        self.name = name
        self.bricksAbove = list()
        self.bricksBelow = list()

    def __repr__(self) -> str:
        start = tuple(a.start for a in self.axes)
        end = tuple(a.end for a in self.axes)
        return f"[Brick '{self.name}' ({start}), ({end})]"

    def intersect(self, other):
        axes = list(a.intersect(b) for a, b in zip(self.axes, other.axes))
        return None if None in axes else Brick(axes)

    def translate(self, delta: tuple):
        self.axes = list(Axis(a.start+d, a.end+d)
                         for a, d in zip(self.axes, delta))


class Implementation:

    def __init__(self, dataPath: str):
        self.bricks = list()

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                start, end = line.strip().split('~')
                start = tuple(int(a) for a in start.split(','))
                end = tuple(int(a) for a in end.split(','))
                axes = list(Axis(a, b) for a, b in zip(start, end))
                name = chr(ord('A') + len(self.bricks) % 26)
                self.bricks.append(Brick(axes, name=name))

        start = tuple(
            min(b.axes[i].start for b in self.bricks) for i in range(3))
        end = tuple(
            max(b.axes[i].end for b in self.bricks) for i in range(3))
        self.axes = list(Axis(a, b) for a, b in zip(start, end))

        # Drop all bricks that have nothing supporting them
        self.bricks.sort(key=lambda a: a.axes[2].start)
        bottomBricks = [
            Brick([self.axes[0], self.axes[1], Axis(0, 0)], name='BOTTOM')]
        bottomZAxis = Axis(0, self.axes[2].end)
        for b1 in self.bricks:
            b1Column = Brick([b1.axes[0], b1.axes[1], bottomZAxis])
            for b2 in bottomBricks:
                section = b1Column.intersect(b2)
                if section is not None:
                    deltaZ = section.axes[2].end - b1.axes[2].start + 1
                    b1.translate((0, 0, deltaZ))
                    self.bricks.sort(key=lambda a: a.axes[2].start)
                    break

            # This should be something more like a heap or a smarter
            # more efficient insertion sort
            bottomBricks.append(b1)
            bottomBricks.sort(key=lambda a: a.axes[2].end, reverse=True)

        # Build all the botom and top relationships
        brickTops, brickBottoms = defaultdict(list), defaultdict(list)
        for b in self.bricks:
            brickTops[b.axes[2].end].append(b)
            brickBottoms[b.axes[2].start].append(b)
        for b1 in self.bricks:
            b1Column = Brick([b1.axes[0], b1.axes[1], self.axes[2]])
            for b2 in brickBottoms[b1.axes[2].end+1]:
                if b1Column.intersect(b2) is not None:
                    b1.bricksAbove.append(b2)
            for b2 in brickTops[b1.axes[2].start-1]:
                if b1Column.intersect(b2) is not None:
                    b1.bricksBelow.append(b2)

    def part1(self):
        return sum(
            not any(b2 for b2 in b1.bricksAbove if len(b2.bricksBelow) == 1)
            for b1 in self.bricks)

    def part2(self):
        def getFallingBrickCount(b: Brick,
                                 resultCache: dict,
                                 disintegratedBrickSet: set):
            resultCacheKey = (b, tuple(disintegratedBrickSet))
            result = resultCache.get(resultCacheKey)
            if result is not None:
                return result

            disintegratedBrickPlusBSet = set.union(disintegratedBrickSet, [b])
            fallingBrickList = list(
                b1 for b1 in b.bricksAbove
                if all(b2 in disintegratedBrickPlusBSet
                       for b2 in b1.bricksBelow))
            disintegratedBrickSet.update(fallingBrickList)
            for b1 in fallingBrickList:
                getFallingBrickCount(b1, resultCache, disintegratedBrickSet)

            resultCache[resultCacheKey] = disintegratedBrickSet
            return disintegratedBrickSet

        return sum(len(getFallingBrickCount(b, dict(), set()))
                   for b in self.bricks)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 5)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 443)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 7)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 69915)
