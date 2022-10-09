
def searchSmart(subset: list, value: int, targetSum: int = 2020):
    """
    Given a SORTED subset of the data to search, find the value that adds
    to the target sum.  Doing this the dumb way would just brute-force the
    list, but we use bisection here since we know it's SORTED.  
    """
    if len(subset) == 0:
        return None
    if value + subset[0] == targetSum:
        return subset[0]
    if value + subset[-1] == targetSum:
        return subset[-1]
    if value + subset[0] > targetSum:
        return None
    if value + subset[-1] < targetSum:
        return None

    medianIndex = len(subset) // 2
    medianValue = subset[medianIndex]
    if value + medianValue > targetSum:
        return searchSmart(subset[:medianIndex], value)
    return searchSmart(subset[medianIndex:], value)


with open('2020/day1.txt') as reader:
    data = sorted(list(int(a) for a in reader.readlines()))

for i, a in enumerate(data):
    b = searchSmart(data[i+1:], a)
    if b is not None:
        print(f"a={a}, b={b}, result={a*b}")
        break

for i, a in enumerate(data):
    for j, b in enumerate(data[i+1:]):
        if a+b < 2020:
            c = searchSmart(data[i+j+1:], a+b)
            if c is not None:
                print(f"a={a}, b={b}, c={c} result={a*b*c}")
                break
