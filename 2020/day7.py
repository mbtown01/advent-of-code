from collections import defaultdict


class Bag:

    def __init__(self, name: str):
        self.name = name
        self.immediateOuterBagsSet = set()
        self.innerBagCountMap = dict()
        self.allOuterBagsSet = set()

    def __repr__(self) -> str:
        return f"[Bag '{self.name}']"

    def findAllOuterBags(self, outerBagSet: set):
        outerBagSet = outerBagSet.union(self.immediateOuterBagsSet)
        for outerBag in self.immediateOuterBagsSet:
            bagSet = outerBag.findAllOuterBags(outerBagSet)
            outerBagSet = outerBagSet.union(bagSet)
        return outerBagSet

    def countTotalInnerBags(self):
        return 1 + sum(b*a.countTotalInnerBags()
                       for a, b in self.innerBagCountMap.items())


with open('2020/day7.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

allBags = dict()


def getBag(bagName: str):
    bag = allBags.get(bagName)
    if bag is None:
        bag = allBags[bagName] = Bag(bagName)
    return bag


for line in allLines:
    outerBagName, innerBagsText = line.split(" bags contain ")
    outerBag = getBag(outerBagName)
    for innerBagText in innerBagsText.split(", "):
        if "no other bags." != innerBagText:
            count, name1, name2, _ = innerBagText.split(" ")
            innerBagName = f"{name1} {name2}"
            innerBag = getBag(innerBagName)
            innerBag.immediateOuterBagsSet.add(outerBag)
            outerBag.innerBagCountMap[innerBag] = int(count)

for bag in allBags.values():
    bag.allOuterBagsSet = bag.findAllOuterBags(set())

shinyGoldBag = allBags['shiny gold']

print(f"part 1: {len(shinyGoldBag.allOuterBagsSet)}")
print(f"part 2: {shinyGoldBag.countTotalInnerBags()-1}")
