import numpy as np
from math import sqrt


_ROTATION_INDICES = [
    [0, 1, 2],
    [0, 2, 1],
    [1, 2, 0],
    [1, 0, 2],
    [2, 0, 1],
    [2, 1, 0],
]
_ROTATION_SIGNS = [
    [+1, +1, +1],
    [+1, +1, -1],
    [+1, -1, +1],
    [+1, -1, -1],
    [-1, +1, +1],
    [-1, +1, -1],
    [-1, -1, +1],
    [-1, -1, -1],
]

ROTATIONS = list((a, b) for b in _ROTATION_INDICES for a in _ROTATION_SIGNS)


class Location:

    def __init__(self, name: str, id: int, location: np.array) -> None:
        self.name = name
        self.id = id
        self.location = location

    def __repr__(self) -> str:
        return f"[{self.name} {self.id:02} ({list(self.location)})]"

    def rotate(self, rotation: int):
        signs, indices = ROTATIONS[rotation]
        location = np.array([self.location[a] for a in indices])
        return Beacon(self.id, location*signs)

    def calcDistance(self, location):
        delta = self.location - location.location
        return sqrt(sum(a**2 for a in delta))


class Beacon(Location):

    def __init__(self, id: int, location: np.array) -> None:
        super().__init__('Beacon', id, location)


class Scanner(Location):

    def __init__(self, id: int) -> None:
        super().__init__('Scanner', id, np.zeros(3))
        self.beaconList = list()
        self._distances = None

    @property
    def distances(self):
        beaconCount = len(self.beaconList)
        prevCount = self._distances.shape[0] if self._distances is not None else 0
        if beaconCount != prevCount:
            distances = np.zeros([beaconCount, beaconCount])
            if prevCount > 0:
                distances[:prevCount, :prevCount] = self._distances
            for i, beacon1 in enumerate(self.beaconList):
                for j in range(i+1, beaconCount):
                    distance = distances[i, j] or \
                        beacon1.calcDistance(self.beaconList[j])
                    distances[j, i] = distances[i, j] = round(distance, 2)
            self._distances = distances

        return self._distances

    def union(self, scanner):
        likelySameList = list()
        for i, beacon1 in enumerate(self.beaconList):
            set1 = set(self.distances[i, :])
            for j, beacon2 in enumerate(scanner.beaconList):
                set2 = set(scanner.distances[j, :])
                commonCount = len(set1.intersection(set2))
                if commonCount >= 12:
                    likelySameList.append((beacon1, beacon2))

        if len(likelySameList) >= 12:
            for rotation in range(len(ROTATIONS)):
                count, thisDistance, finalDistance = 0, None, None
                for beacon1, beacon2 in likelySameList:
                    count, finalDistance = count+1, thisDistance
                    rotatedBeacon = beacon2.rotate(rotation)
                    thisDistance = beacon1.location + rotatedBeacon.location
                    if finalDistance is not None:
                        if any(finalDistance != thisDistance):
                            break

                if all(thisDistance == finalDistance):
                    scanner.location = finalDistance
                    intersectedBeacons = list(a[1] for a in likelySameList)
                    for beacon in scanner.beaconList:
                        relativeBeacon = beacon.rotate(rotation)
                        relativeBeacon.location = \
                            finalDistance - relativeBeacon.location
                        if beacon not in intersectedBeacons:
                            self.beaconList.append(relativeBeacon)
                    return True

        return False


scannerList = list()
with open('2021/day19.txt') as reader:
    for line in reader.readlines():
        line = line.strip()
        if line.startswith('--- scanner'):
            id = len(scannerList)
            scannerList.append(Scanner(id))
        elif ',' in line:
            scanner = scannerList[-1]
            id = len(scanner.beaconList)
            location = np.array([int(a) for a in line.split(',')])
            beacon = Beacon(id, location)
            scanner.beaconList.append(beacon)

allScanners = list(scannerList)
while(len(scannerList) > 1):
    for scanner in list(scannerList[1:]):
        if scannerList[0].union(scanner):
            scannerList.remove(scanner)

print(f"part 1: {len(scannerList[0].beaconList)}")

scannerCount = len(allScanners)
distance = np.zeros((scannerCount, scannerCount), dtype=np.int32)
for i, scanner1 in enumerate(allScanners):
    for j in range(i+1, scannerCount):
        scanner2 = allScanners[j]
        distance[j, i] = distance[i, j] = \
            sum(np.abs(scanner1.location - scanner2.location))

print(f"part 2: {np.max(distance)}")
