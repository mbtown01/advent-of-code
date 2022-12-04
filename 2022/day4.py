

def isTotal(r1l: int, r1r: int, r2l: int, r2r: int):
    return ((r1l <= r2l and r1r >= r2r) or
            (r2l <= r1l and r2r >= r1r))


def isPartial(r1l: int, r1r: int, r2l: int, r2r: int):
    return ((r1r >= r2l and r1r <= r2r) or
            (r1l >= r2l and r1l <= r2r) or
            (r1l >= r2l and r1r <= r2r) or
            (r1l <= r2l and r1r >= r2r))


part1, part2 = 0, 0
with open('2022/day4.txt') as reader:
    for line in (a.strip() for a in reader.readlines()):
        (r1l, r1r), (r2l, r2r) = \
            list([int(b) for b in a.split('-')] for a in line.split(','))
        part1 += 1 if isTotal(r1l, r1r, r2l, r2r) else 0
        part2 += 1 if isPartial(r1l, r1r, r2l, r2r) else 0

print(f"part 1: {part1}")
print(f"part 2: {part2}")
