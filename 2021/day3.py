import numpy as np


def decodePart2(allNumbers: list, useMostCommon: bool, tieBreaker: str):
    filteredNumbers = allNumbers.copy()
    for i in range(len(allNumbers[0])):
        if len(filteredNumbers) > 1:
            oneCount = sum(1 if a[i] == '1' else 0 for a in filteredNumbers)
            if oneCount > len(filteredNumbers)/2:
                selector = '1' if useMostCommon else '0'
            elif oneCount < len(filteredNumbers)/2:
                selector = '0' if useMostCommon else '1'
            else:
                selector = tieBreaker
            filteredNumbers = list(
                a for a in filteredNumbers if selector == a[i])

    if len(filteredNumbers) != 1:
        raise RuntimeError("filteredNumbers len != 1")

    return int(filteredNumbers[0], 2)


with open('2021/day3.txt') as reader:
    allNumbers = list(a.strip() for a in reader.readlines())
    countList = list()
    for i in range(len(allNumbers[0])):
        countList.append(sum(1 if a[i] == '1' else 0 for a in allNumbers))

    gammaStr = ''.join(list(
        '1' if a > len(allNumbers)/2 else '0' for a in countList))
    gamma = int(gammaStr, 2)
    epsilonStr = ''.join(list(
        '0' if a > len(allNumbers)/2 else '1' for a in countList))
    epsilon = int(epsilonStr, 2)
    consumption = gamma*epsilon

    print(
        f'part 1: gamma={gamma}, epsilon={epsilon}, consumption={consumption}')

    o2Value = decodePart2(allNumbers, True, '1')
    co2Value = decodePart2(allNumbers, False, '0')
    rating = o2Value*co2Value

    print(f'part 2: o2Value={o2Value}')
    print(f'part 2: co2Value={co2Value}')
    print(f'part 2: rating={rating}')
