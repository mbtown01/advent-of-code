from collections import defaultdict
from math import factorial
from itertools import permutations


bruteForceCache = dict()


def bruteForce(length: int):
    """ I never figured out an equation that would simply calculate 
    this, so we are brute forcing the search by doing ALL POSSIBLE
    permutations of a jolt being in the sequence, and then simply
    eliminating ANYTHING that has a sequence of 3 or more.  Not beautiful
    but seems it isn't compute intensive enough to be a big deal """
    count = bruteForceCache.get(length)
    if count is not None:
        return count

    sequence = list(range(length))
    count = 0
    for i in range(2**length):
        sequence = bin(i)[2:]
        sequence = '0'*(length-len(sequence)) + sequence
        if '000' not in sequence:
            count += 1
    return count


if __name__ == '__main__':

    with open('2020/day10.txt') as reader:
        numbers = list(int(a.strip()) for a in reader.readlines())

    sortedNumbers = sorted(numbers)
    sortedNumbers = [0, *sortedNumbers, max(sortedNumbers) + 3]
    deltas = list(
        sortedNumbers[i] - sortedNumbers[i-1] for i in range(1, len(sortedNumbers)))
    deltaSumsMap = defaultdict(int)
    for value in deltas:
        deltaSumsMap[value] += 1

    final1 = deltaSumsMap[3] * deltaSumsMap[1]
    print(f"part 1: {final1}")

    currentSequenceCount = 0
    final2 = 1
    for delta in deltas:
        if delta == 1:
            currentSequenceCount += 1
        else:
            if currentSequenceCount > 1:
                final2 *= bruteForce(currentSequenceCount-1)
            currentSequenceCount = 0

    print(f"part 2: {final2}")

    for i in range(0, 8):
        real = bruteForce(i+1)
        test = testCombinations(i+1)
        print(f"For i={i+1}, real={real}, test={test}, foo={2**(i+1)-real}")

    print("done")
