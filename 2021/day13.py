import numpy as np

dotList, foldList = list(), list()
with open('day13.txt') as reader:
    for line in reader.readlines():
        line = line.strip()
        if ',' in line:
            dotList.append(list(int(a) for a in line.split(',')))
        if line.startswith('fold'):
            line = line.replace('fold along ', '')
            axis, value = line.split('=')
            foldList.append((axis, int(value)))

nx = max(a[0] for a in dotList)+1
ny = max(a[1] for a in dotList)+1
paper = np.zeros((ny, nx), np.byte)

for x, y in dotList:
    paper[y, x] = 1

for i, (axis, value) in enumerate(foldList):
    if axis == 'x':
        paper = paper.transpose()
        ny, nx = nx, ny
    newPaper = np.zeros((ny//2, nx), np.byte)
    for y in range(ny//2):
        for x in range(nx):
            newPaper[y, x] = 1 if paper[y, x] + paper[ny-y-1, x] > 0 else 0
    ny = ny // 2
    paper = newPaper

    if axis == 'x':
        paper = paper.transpose()
        ny, nx = nx, ny

    print(f"fold {i+1}, count={paper.sum()}")

for y in range(ny):
    print((''.join(list('#' if a else ' ' for a in paper[y, :]))))
