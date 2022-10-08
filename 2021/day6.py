import numpy as np

with open('day6.txt') as reader:
    allFish = list(int(a) for a in reader.readline().strip().split(','))
    allFish = np.array(allFish)
    allFishBuckets = list()
    for bucket in range(8+1):
        allFishBuckets.append(sum(
            list(1 if bucket == a else 0 for a in allFish)))

    for day in range(256):
        spawnCount = allFishBuckets[0]
        allFishBuckets = allFishBuckets[1:] + [0]
        allFishBuckets[6] += spawnCount
        allFishBuckets[8] += spawnCount

    result = sum(allFishBuckets)
    print(f"part 1: result={result}")
