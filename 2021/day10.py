

TOKEN_MAP = {
    '<': '>',
    '(': ')',
    '[': ']',
    '{': '}',
}

TOKEN_SCORE = {
    '>': 25137,
    ')': 3,
    ']': 57,
    '}': 1197,
}

CLOSER_SCORE = {
    '>': 4,
    ')': 1,
    ']': 2,
    '}': 3,
}

OPENERS = list(TOKEN_MAP.keys())
CLOSERS = list(TOKEN_MAP.values())


def parse(line):
    tokenStack = list()
    for token in list(a for a in line.strip()):
        if token in OPENERS:
            tokenStack.append(TOKEN_MAP[token])
        if token in CLOSERS:
            if len(tokenStack) == 0:
                raise RuntimeError('Closure with no opener')
            if token != tokenStack[-1]:
                return (False, TOKEN_SCORE[token])
            tokenStack = tokenStack[:-1]

    score = 0
    for token in reversed(tokenStack):
        score = score*5 + CLOSER_SCORE[token]

    return (True, score)


with open('day10.txt') as reader:
    total, scoreList = 0, list()
    for line in reader.readlines():
        line = line.strip()
        incomplete, score = parse(line)
        if incomplete:
            scoreList.append(score)
        else:
            total += score

    print(f"part 1: score={total}")
    part2Score = sorted(scoreList)[len(scoreList)//2]
    print(f"part 2: score={part2Score}")
