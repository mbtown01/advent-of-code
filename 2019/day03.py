import unittest
from os import path


class Segment:

    def __init__(self, p1Steps: int, p1: tuple, p2: tuple):
        self.p1Steps = p1Steps
        self.y1, self.x1 = p1
        self.y2, self.x2 = p2
        self.isHorizontal = self.y1 == self.y2

    def __repr__(self):
        return f"[Segment ({self.y1},{self.x1}) - ({self.y2},{self.x2})]"

    def getIntersection(self, other):
        hSeg, vSeg = (self, other) if self.isHorizontal else (other, self)
        hx1, hx2 = (hSeg.x1, hSeg.x2) if hSeg.x1 < hSeg.x2 \
            else (hSeg.x2, hSeg.x1)
        vy1, vy2 = (vSeg.y1, vSeg.y2) if vSeg.y1 < vSeg.y2 \
            else (vSeg.y2, vSeg.y1)

        if hx1 < vSeg.x1 < hx2 and vy1 < hSeg.y1 < vy2:
            return (hSeg.y1, vSeg.x1)
        return None

    def getStepsToPoint(self, point: tuple):
        dy = abs(self.y1 - point[0])
        dx = abs(self.x1 - point[1])
        return self.p1Steps + dx + dy

    def getMinSteps(self, other):
        if (i := self.getIntersection(other)) is not None:
            return self.getStepsToPoint(i) + other.getStepsToPoint(i)
        return None


class Implementation:

    def __init__(self, dataPath: str):
        segVecMap = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

        self.pathList = list()

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                segList, prevLoc, p1Steps = list(), (0, 0), 0
                for segment in line.strip().split(','):
                    segVec, segLen = segVecMap[segment[0]], int(segment[1:])
                    nextLoc = tuple(
                        p + s*segLen for p, s in zip(prevLoc, segVec))
                    segList.append(Segment(p1Steps, prevLoc, nextLoc))
                    prevLoc, p1Steps = nextLoc, p1Steps + segLen
                self.pathList.append(segList)

    def part1(self):
        intersections = list(r for a in self.pathList[0]
                             for b in self.pathList[1]
                             if (r := a.getIntersection(b)) is not None)
        return min(abs(r[0])+abs(r[1]) for r in intersections)

    def part2(self):
        distances = list(r for a in self.pathList[0]
                         for b in self.pathList[1]
                         if (r := a.getMinSteps(b)) is not None)
        return min(distances)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_intersect1(self):
        s1 = Segment(0, (0, 0), (0, 10))
        s2 = Segment(0, (-10, 5), (10, 5))
        result = s1.getIntersection(s2)
        self.assertEqual(result, (0, 5))

    def test_intersect2(self):
        s1 = Segment(0, (0, 0), (0, 10))
        s2 = Segment(0, (-10, 5), (10, 5))
        result = s2.getIntersection(s1)
        self.assertEqual(result, (0, 5))

    def test_part1_ex1(self):
        impl = Implementation(f'{self._pathPrefix}_example1.txt')
        result = impl.part1()
        self.assertEqual(result, 6)

    def test_part1_ex2(self):
        impl = Implementation(f'{self._pathPrefix}_example2.txt')
        result = impl.part1()
        self.assertEqual(result, 159)

    def test_part1_ex3(self):
        impl = Implementation(f'{self._pathPrefix}_example3.txt')
        result = impl.part1()
        self.assertEqual(result, 135)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 258)

    def test_part2_ex1(self):
        impl = Implementation(f'{self._pathPrefix}_example1.txt')
        result = impl.part2()
        self.assertEqual(result, 30)

    def test_part2_ex2(self):
        impl = Implementation(f'{self._pathPrefix}_example2.txt')
        result = impl.part2()
        self.assertEqual(result, 610)

    def test_part2_ex3(self):
        impl = Implementation(f'{self._pathPrefix}_example3.txt')
        result = impl.part2()
        self.assertEqual(result, 410)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 12304)
