import numpy as np
from collections import defaultdict

template, ruleMap = None, dict()
with open('2021/day14.txt') as reader:
    for line in reader.readlines():
        line = line.strip()
        if '->' in line:
            key, value = line.split(' -> ')
            ruleMap[key] = value
        elif len(line) > 0:
            template = line


def executeStep(pairMap: dict, distribution: dict):
    result = defaultdict(int)
    for pair, count in pairMap.items():
        ruleChar = ruleMap.get(pair)
        if ruleChar is not None:
            distribution[ruleChar] += count
            result[pair[0]+ruleChar] += count
            result[ruleChar+pair[1]] += count
        else:
            result[pair] += count
    return result


distribution, pairMap = defaultdict(int), defaultdict(int)
for pair in list(a+b for a, b in zip(template[:-1], template[1:])):
    pairMap[pair] += 1
    distribution[pair[0]] += 1
distribution[template[-1]] += 1

for i in range(40):
    pairMap = executeStep(pairMap, distribution)
    counts = sorted(distribution.values())
    print(f"part 1/2: iter {i}: {sum(counts)} [{counts[-1]-counts[0]}]")
