

itemScore = {chr(a): a-ord('a')+1 for a in range(ord('a'), ord('z')+1)}
itemScore.update({chr(a): a-ord('A')+27 for a in range(ord('A'), ord('Z')+1)})

with open('2022/day3.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

total = 0
for line in allLines:
    c1, c2 = line[:len(line)//2], line[len(line)//2:]
    common = set(c1).intersection(c2)
    total += sum(itemScore[a] for a in common)
print(f"part 1: {total}")

total = 0
for i in range(0, len(allLines), 3):
    l1, l2, l3 = allLines[i:i+3]
    common = set(l1).intersection(l2).intersection(l3)
    total += sum(itemScore[a] for a in common)
print(f"part 2: {total}")
