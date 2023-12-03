
part1Max = {'red': 12, 'green': 13, 'blue': 14}
part1Sum, part2Sum = 0, 0
with open('2023/day2.txt', encoding="utf8") as reader:
    for line in reader:
        gameText, drawText = line.strip().split(': ')
        gameId = int(gameText.split(' ')[1])

        gameCubeCountList = [
            {p[1]: int(p[0]) for p in list(
                t.split(' ') for t in s.split(', '))}
            for s in drawText.split('; ')
        ]
        possible = all(
            count <= part1Max[color]
            for gameCubeCount in gameCubeCountList
            for color, count in gameCubeCount.items()
        )
        if possible:
            part1Sum += gameId

        colorCounts = {a: 0 for a in part1Max}
        for gameCubeCount in gameCubeCountList:
            for color, count in gameCubeCount.items():
                colorCounts[color] = max(colorCounts[color], count)
        localProduct = 1
        for count in colorCounts.values():
            localProduct *= count
        part2Sum += localProduct

    print(f"part 1: {part1Sum}")
    print(f"part 2: {part2Sum}")
