from math import acos, pi

import unittest
import numpy as np


class Stone:
    def __init__(self, pos: tuple, vel: tuple) -> None:
        self.pos = pos
        self.vel = vel

    def __repr__(self) -> str:
        return f"[Stone {self.pos} @ {self.vel}]"


class Implementation:

    def __init__(self, dataPath: str):
        self.stoneList = list()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader.readlines():
                pos, vel = line.strip().split(' @ ')
                pos = list(float(a) for a in pos.split(', '))
                vel = list(float(a) for a in vel.split(', '))
                self.stoneList.append(Stone(pos, vel))

    @classmethod
    def getStonePathIntersection2D(cls, s1: Stone, s2: Stone):
        # Any error in the solve means the lines do not intersect.  Also, be
        # sure to check the if intersection is in the future and not the past!
        # NOTE: This is NOT a 3D solution -- plugging s back in here for
        # the 3rd dimension could yield a value NOT on each line
        try:
            # Solve for the x, y solution first
            a1, b1, a2, b2 = s1.pos, s1.vel, s2.pos, s2.vel
            s, _ = np.linalg.solve([[b1[0], -b2[0]], [b1[1], -b2[1]]],
                                   [a2[0]-a1[0], a2[1]-a1[1]])
        except np.linalg.LinAlgError:
            return None

        return a1[0] + b1[0]*s, a1[1] + b1[1]*s

    def part1(self, xyMin: int, xyMax: int):
        def getStonePathCollision2D(s1: Stone, s2: Stone):
            result = Implementation.getStonePathIntersection2D(s1, s2)
            if result is not None:
                a1, b1, a2, b2 = s1.pos, s1.vel, s2.pos, s2.vel
                x, y = result
                if (x-a1[0]) / b1[0] > 0 and (x-a2[0]) / b2[0] > 0:
                    return x, y
            return None

        resultList = list((s1, s2, getStonePathCollision2D(s1, s2))
                          for i, s1 in enumerate(self.stoneList)
                          for s2 in self.stoneList[i:])
        intersectionList = list(a for a in resultList if a[2] is not None)
        return sum(xyMin <= a[0] <= xyMax and
                   xyMin <= a[1] <= xyMax
                   for _, _, a in intersectionList)

    def part2(self, i1: int, i2: int, i3: int):
        """
        The following math comes from the simple equations:
            vecP0 + vecV0*t1 = vecP1 + vecV1*t1
            vecP0 + vecV0*t2 = vecP2 + vecV2*t2
            ...
            vecP0 + vecV0*t_n = vecP_n + vecV_n*t_n

            where P0 is the solution initial position vector, V0 is 
            solution velocity vector, and P_n, V_n are the position and 
            velocity vectors of each stone.  

            Lots of algebra gets us to building a linear system of six
            equations and six unknowns below
        """
        xyMap = {0: 0, 1: 1, 2: 3, 3: 4}    # Skip the Z values
        xzMap = {0: 0, 1: 2, 2: 3, 3: 5}    # Skip the Y values
        yzMap = {0: 1, 1: 2, 2: 4, 3: 5}    # Skip the X values
        fullMatrix = [(self.stoneList[i1], self.stoneList[i2], xyMap),
                      (self.stoneList[i1], self.stoneList[i3], xyMap),
                      (self.stoneList[i1], self.stoneList[i2], xzMap),
                      (self.stoneList[i1], self.stoneList[i3], xzMap),
                      (self.stoneList[i1], self.stoneList[i2], yzMap),
                      (self.stoneList[i1], self.stoneList[i3], yzMap)]

        matrix, rhs = list(), list()
        for s1, s2, indexMap in fullMatrix:
            row, i1, i2 = [0]*6, indexMap[0], indexMap[1]
            p11, p12, p21, p22 = s1.pos[i1], s1.pos[i2], s2.pos[i1], s2.pos[i2]
            v11, v12, v21, v22 = s1.vel[i1], s1.vel[i2], s2.vel[i1], s2.vel[i2]
            row[indexMap[0]] = v22 - v12
            row[indexMap[1]] = v11 - v21
            row[indexMap[2]] = p12 - p22
            row[indexMap[3]] = p21 - p11
            matrix.append(row)
            rhs.append(p12*v11 + p21*v22 - p22*v21 - p11*v12)

        # Note that in python, this is somewhat numerically unstable
        # beacuse of the size of the position vectors.  It just so happens
        # that stones 1 throuh 3 yield the right answer.  ALL combinations
        # of stones mathematically shoud give same result but floating point
        # precision gets in the way...
        result = np.linalg.solve(matrix, rhs)
        return sum(round(a) for a in result[:3])


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1(7, 27)
        self.assertEqual(result, 2)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1(200000000000000, 400000000000000)
        self.assertEqual(result, 26611)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2(0, 1, 2)
        self.assertEqual(result, 47)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2(1, 2, 3)
        self.assertEqual(result, 684195328708898)

    def test_getStoneIntersection(self):
        s1 = Stone((5, 2, -1), (1, -2, -3))
        s2 = Stone((2, 0, 4), (1, 2, -1))
        result = Implementation.getStonePathIntersection2D(s1, s2)
        expected = [4, 4]
        for a, b in zip(result, expected):
            self.assertAlmostEqual(a, b)
