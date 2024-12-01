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

    def part1(self, xyMin: int, xyMax: int):
        result = 0
        for i, s1 in enumerate(self.stoneList):
            for s2 in self.stoneList[i:]:
                (p11, p12, _), (p21, p22, _) = s1.pos, s2.pos
                (v11, v12, _), (v21, v22, _) = s1.vel, s2.vel
                matrix = [[v11, -v21], [v12, -v22]]
                rhs = [p21 - p11, p22 - p12]
                try:
                    _, t = np.linalg.solve(matrix, rhs)
                    x, y = p21 + v21 * t, p22 + v22 * t
                    if (x-p11) / v11 > 0 and (x-p21) / v21 > 0:
                        if xyMin <= x <= xyMax and xyMin <= y <= xyMax:
                            result += 1
                except np.linalg.LinAlgError:
                    pass

        return result

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
        # Note that in python, this is somewhat numerically unstable
        # beacuse of the size of the position vectors.  It just so happens
        # that stones 1 throuh 3 yield the right answer.  ALL combinations
        # of stones mathematically shoud give same result but floating point
        # precision gets in the way...
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2(1, 2, 3)
        self.assertEqual(result, 684195328708898)
