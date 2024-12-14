import unittest
from os import path
from collections import defaultdict


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.data = list(int(a) for a in reader.readline().strip())

    def defrag(self, data: list):
        result = list(dict(val=a[0], index=i, count=a[1], data=list())
                      for i, a in enumerate(data))
        spaceListMap = defaultdict(list)
        for value in [a for a in result if a['val'] is None]:
            spaceListMap[value['count']].append(value)

        for mover in list(a for a in result if a.get('val') is not None)[::-1]:
            availSpaces = list(b for a, b in spaceListMap.items()
                               if a >= mover['count'] and
                               b[0]['index'] < mover['index'])
            if len(availSpaces) > 0:
                space = sorted(availSpaces, key=lambda a: a[0]['index'])[0][0]
                space['data'].append(mover.copy())
                mover['val'] = None
                spaceListMap[space['count']].pop(0)
                if len(spaceListMap[space['count']]) == 0:
                    del spaceListMap[space['count']]
                space['count'] -= mover['count']
                if space['count'] > 0:
                    spaceListMap[space['count']].append(space)
                    spaceListMap[space['count']].sort(key=lambda a: a['index'])

        index, checksum = 0, 0
        for entry in (a for b in (a['data'] + [a] for a in result) for a in b):
            if entry['val'] is not None:
                for i in range(entry['count']):
                    checksum += entry['val']*(index+i)
            index += entry['count']

        return checksum

    def part1(self):
        data = list((None if i % 2 else i//2, 1)
                    for i, a in enumerate(self.data) for _ in range(a))
        return self.defrag(data)

    def part2(self):
        data = list((None if i % 2 else i//2, a)
                    for i, a in enumerate(self.data))
        return self.defrag(data)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 1928)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 6385338159127)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 2858)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 6415163624282)
