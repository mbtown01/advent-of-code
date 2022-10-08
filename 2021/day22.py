from functools import reduce
from itertools import product


def minmax(a, b):
    return (a, b) if a < b else (b, a)


class Axis:

    def __init__(self, a: int, b: int) -> None:
        self.min, self.max = minmax(a, b)

    def __repr__(self) -> str:
        return f"[Axis ({self.min}..{self.max})]"

    def __str__(self) -> str:
        return f"{self.min}..{self.max}"

    def __eq__(self, other: object) -> bool:
        return other is not None and \
            self.min == other.min and \
            self.max == other.max

    def __lt__(self, other: object) -> bool:
        if self.min == other.min:
            return self.max < other.max
        return self.min < other.min

    @property
    def len(self):
        return self.max - self.min + 1

    def intersectUnion(self, other):
        uMin, iMin = minmax(self.min, other.min)
        iMax, uMax = minmax(self.max, other.max)
        if iMin <= iMax:
            return [Axis(iMin, iMax), Axis(uMin, uMax)]

    def intersect(self, other):
        result = self.intersectUnion(other)
        if result is not None:
            return result[0]

    def union(self, other):
        result = self.intersectUnion(other)
        if result is not None:
            return result[1]

    def combine(self, other):
        # The combination of identical axes is pure intersection
        if self == other:
            return [None, self, None]

        # If there is no union, then there is no intersection, so just return
        # the left and right in the appropriate order
        intersectUnion = self.intersectUnion(other)
        if intersectUnion is None:
            left, right = minmax(self, other)
            return [left, None, right]

        # figure out the rest of the axis, which could see left or right
        # fully in the intersection region
        intersection, union = intersectUnion
        result = [None, intersection, None]
        if union.min != intersection.min:
            result[0] = Axis(union.min, intersection.min-1)
        if union.max != intersection.max:
            result[2] = Axis(intersection.max+1, union.max)

        return result


class Region:

    def __init__(self, axes: list):
        self.axes = axes

    def __eq__(self, other: object) -> bool:
        return other is not None and all(
            a == b for a, b in zip(self.axes, other.axes))

    def intersect(self, other):
        assert(len(self.axes) == len(other.axes))
        axes = list(a.intersect(b) for a, b in zip(self.axes, other.axes))
        if None not in axes:
            return Region(axes)

    @property
    def size(self):
        return reduce(lambda a, b: a*b, (a.len for a in self.axes))


class RegionWithState(Region):

    def __init__(self, axes: list, isOn: bool):
        super().__init__(axes)
        self.isOn = isOn

    def chomp(self, other):
        """ Take this cube and chomp a byte with 'other' cube, returning
        the unique subcubes that result """

        if self.intersect(other) is None:
            return [self]

        subRegions = list()
        axisProduct = product(*list(
            a.combine(other.axes[i]) for i, a in enumerate(self.axes)))
        for axes in (p for p in axisProduct if None not in p):
            region = Region(axes)
            if self.intersect(region) is not None:
                if other.intersect(region) is None:
                    subRegions.append(type(self)(axes, self.isOn))
        return subRegions


class Rectangle(RegionWithState):

    def __init__(self, axes: list, isOn: bool):
        assert(len(axes) == 2)
        super().__init__(axes, isOn)

    def __repr__(self) -> str:
        return f"[Rectangle {'on' if self.isOn else 'off'} " \
            f"x={self.axes[0]},y={self.axes[1]}]"


class Cube(RegionWithState):

    def __init__(self, axes: list, isOn: bool):
        assert(len(axes) == 3)
        super().__init__(axes, isOn)

    def __repr__(self) -> str:
        return f"[Cube {'on' if self.isOn else 'off'} " \
            f"x={self.axes[0]},y={self.axes[1]},z={self.axes[2]}]"


def findSum(universe: Region):
    allCubes = list()
    with open('day22.txt') as reader:
        for line in reader.readlines():
            state, cubeDef = line.strip().split(' ')
            axes = list()
            for axis in cubeDef.split(','):
                axisMin, axisMax = tuple(int(a) for a in axis[2:].split('..'))
                axes.append(Axis(axisMin, axisMax))
            thisCube = Cube(axes, state == 'on')

            if universe is None or universe.intersect(thisCube) != None:
                updatedCubes = list()
                for cube in allCubes:
                    updatedCubes += cube.chomp(thisCube)
                if thisCube.isOn:
                    updatedCubes.append(thisCube)
                allCubes = updatedCubes

    return sum(a.size for a in allCubes)


universe = Region(
    [Axis(-50, 50),
     Axis(-50, 50),
     Axis(-50, 50)],
)
# universe = None

part1 = findSum(universe)
print(f"part 1: {part1}")

part2 = findSum(None)
print(f"part 2: {part2}")
