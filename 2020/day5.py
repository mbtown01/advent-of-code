
if __name__ == '__main__':

    with open('2020/day5.txt') as reader:
        allLines = list(a.strip() for a in reader.readlines())

    maxSeatId = 0
    allSeatIds = list()
    for line in allLines:
        row, col = line[:7], line[7:]
        rowNumBin = row.replace('F', '0').replace('B', '1')
        colNumBin = col.replace('L', '0').replace('R', '1')
        rowNum, colNum = int(rowNumBin, 2), int(colNumBin, 2)
        seatId = rowNum*8 + colNum
        maxSeatId = max(maxSeatId, seatId)
        allSeatIds.append(seatId)

    print(f"Max seatId = {maxSeatId}")

    allSeatIds = sorted(allSeatIds)
    deltas = list(
        allSeatIds[i+1] - allSeatIds[i] for i in range(len(allSeatIds)-1))
    for i, delta in enumerate(deltas):
        if delta == 2:
            print(f"missing seat is {allSeatIds[i]+1}")
