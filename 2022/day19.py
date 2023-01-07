from enum import Enum
from collections import defaultdict
from itertools import product


class Resource(Enum):
    ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3

    @classmethod
    def fromString(cls, text: str):
        if text == 'ore':
            return Resource.ORE
        if text == 'clay':
            return Resource.CLAY
        if text == 'obsidian':
            return Resource.OBSIDIAN
        if text == 'geode':
            return Resource.GEODE
        raise RuntimeError(f"Unknown resource '{text}'")


class ResourceCountCollection(dict):

    def __init__(self, resources: dict = None) -> None:
        if resources is not None:
            self.update(resources)

    def __repr__(self) -> str:
        resourcePairs = list(
            f"{a.name}: {b}" for (a, b) in self.items())
        return f"[ResourceCountCollection ({', '.join(resourcePairs)})]"

    def _buildSharedKeys(self, other: object):
        return set([*self.keys(), *other.keys()])

    def copy(self):
        return ResourceCountCollection(super().copy())

    def __add__(self, other: object):
        result = {a: self.get(a, 0) + other.get(a, 0)
                  for a in self._buildSharedKeys(other)}
        return ResourceCountCollection(result)

    def __sub__(self, other: object):
        result = {a: self.get(a, 0) - other.get(a, 0)
                  for a in self._buildSharedKeys(other)}
        return ResourceCountCollection(result)


class BluePrint:

    def __init__(self, id: int) -> None:
        self.id = id
        self.robotCosts = defaultdict(ResourceCountCollection)

    def __repr__(self) -> str:
        return f"[BluePrint {self.id}]"

    def findQuality(self, resources: ResourceCountCollection,
                    robots: ResourceCountCollection,
                    seen: dict, best: int, remain: int):
        # if remain == 0:
        #     return resources.get(Resource.GEODE, 0)
        seenKey = tuple(
            [resources.get(a, 0) for a in Resource] +
            [robots.get(a, 0) for a in Resource])
        seenRemain = seen.get(seenKey, 0)
        if remain <= seenRemain:
            return best

        print(f"{remain} robots: {robots}")
        print(f"{remain} resources: {resources}")

        resourceCount = 0
        for resource, robotCost in self.robotCosts.items():
            nextResources, steps = resources.copy(), 1
            while steps < remain and any(
                    nextResources.get(a, 0) < b for (a, b) in robotCost.items()):
                steps, nextResources = steps + 1, nextResources + robots
            if steps < remain:
                print(f"{remain} BUILDING {resource} {steps} {robotCost}")
                scenarioResult = self.findQuality(
                    (nextResources - robotCost) + robots,
                    robots + ResourceCountCollection({resource: 1}),
                    seen, best, remain-steps)
                if best < scenarioResult:
                    print(f"new best {scenarioResult} remain={remain}")
                best = max(best, scenarioResult)
                resourceCount += 1

        if resourceCount == 0:
            best = resources.get(Resource.GEODE, 0) + \
                robots.get(Resource.GEODE, 0) * remain

        seen[seenKey] = remain
        return best


bluePrintList = list()
with open('2022/day19.txt') as reader:
    lines = list(a.strip() for a in reader.readlines())
    lines = list(a for a in lines if len(a) and not a.startswith('#'))
    for line in lines:
        blueprintDesc, instructionsDesc = line.split(': ')
        bluePrintList.append(BluePrint(int(blueprintDesc.split(' ')[1])))
        components = list(
            a.strip() for a in instructionsDesc.strip().split('.') if len(a))
        for component in components:
            robotDesc, resourcesDesc = component.split(' costs ')
            robotType = Resource.fromString(robotDesc.split(' ')[1])
            for resourceDesc in resourcesDesc.split(' and '):
                count, resource = resourceDesc.split(' ')
                count, resource = int(count), Resource.fromString(resource)
                bluePrintList[-1].robotCosts[robotType][resource] = count

totalQuality = 0
for bluePrint in bluePrintList:
    result = bluePrint.findQuality(
        ResourceCountCollection(),
        ResourceCountCollection({Resource.ORE: 1}), dict(), 0, 24)
    quality = bluePrint.id * result
    print(f"{bluePrint.id}: {result} quality={quality}")
    totalQuality += quality

print(f"part 1: {totalQuality}")
