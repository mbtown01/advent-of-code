digitWords = \
    ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
digitWordMap = {str(a+1): b for (a, b) in enumerate(digitWords)}

p1sum, p2sum = 0, 0
with open('2023/day1.txt', encoding="utf8") as reader:
    for line in reader:
        digits = list(int(a) for a in line if a in digitWordMap)
        if len(digits) > 0:
            p1sum += 10*digits[0] + digits[-1]

        findResults = \
            [(a, line.find(a)) for a in digitWordMap] + \
            [(a, line.find(b)) for a, b in digitWordMap.items()] + \
            [(a, line.rfind(a)) for a in digitWordMap] + \
            [(a, line.rfind(b)) for a, b in digitWordMap.items()]
        findResults = list(a for a in findResults if a[1] != -1)
        findResults = sorted(findResults, key=lambda a: a[1])
        if len(findResults) > 0:
            p2sum += 10*int(findResults[0][0]) + int(findResults[-1][0])

    print(f"part 1: {p1sum}")
    print(f"part 2: {p2sum}")
