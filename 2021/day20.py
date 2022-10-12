import numpy as np

with open('2021/day20.txt') as reader:
    algorithm = reader.readline().strip()
    reader.readline()

    imageRows = list()
    line = reader.readline().strip()
    while len(line):
        imageRows.append(line.strip())
        line = reader.readline().strip()


def halo(input: np.array, value: int = 0):
    nj, ni = input.shape
    output = np.zeros((nj+2, ni+2)) + value
    output[1:-1, 1:-1] = input
    return output


decoder = np.array([1 if a == '#' else 0 for a in algorithm])
image = np.zeros([len(imageRows[0]), len(imageRows)])
for i, row in enumerate(imageRows):
    image[i, :] = np.array([1 if a == '#' else 0 for a in row])
image = halo(image)


def sharpen(input: np.array, iter: int):
    output = np.zeros(input.shape)
    nj, ni = output.shape
    input = halo(input, input[0, 0])
    for j in range(nj):
        for i in range(ni):
            numbers = np.concatenate(list(input[j:j+3, i:i+3]))
            index = int(''.join('1' if a else '0' for a in numbers), 2)
            output[j, i] = decoder[index]

    return halo(output, iter)


def display(image: np.array):
    nj, ni = image.shape
    for j in range(nj):
        print(''.join('#' if a else '.' for a in image[j, :]))


for i in range(50):
    image = sharpen(image, 0 if i % 2 else decoder[0])

display(image)

print(f"part 1: {int(image.sum())}")
# 5591 too high
