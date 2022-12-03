elfCalorieList = [0]

with open('2022/day1.txt') as reader:
    for line in reader.readlines():
        try:
            elfCalorieList[-1] += int(line.strip())
        except:
            elfCalorieList.append(0)

print(f"part 1: {max(elfCalorieList)}")
print(f"part 2: {sum(sorted(elfCalorieList)[-3:])}")
