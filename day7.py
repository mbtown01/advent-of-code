import numpy as np

with open('day7.txt') as reader:
    allCrabs = list(int(a) for a in reader.readline().strip().split(','))
    assert 0 == min(allCrabs)
    posListLen = max(allCrabs)+1
    posList = [0] * posListLen
    for crabPos in allCrabs:
        posList[crabPos] += 1

    posEnumList = list((i, a) for i, a in enumerate(posList) if a > 0)

    # scoreList = list()
    # for pos in range(posListLen):
    #     scoreList.append(
    #         (pos, sum(list(a*abs(pos-i) for i, a in posEnumList))))

    # result = sorted(scoreList, key=lambda a: a[1])[0]
    # print(f"part 1: result={result}")

    def score(a: int):
        return a*(a+1)//2

    scoreList = list()
    for pos in range(posListLen):
        scoreList.append(
            (pos, sum(list(a*score(abs(pos-i)) for i, a in posEnumList))))

    result = sorted(scoreList, key=lambda a: a[1])[0]
    print(f"part 2: result={result}")
