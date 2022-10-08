import numpy as np


with open('day1.txt') as reader:
    data = list(int(a) for a in reader.readlines())
    increments = sum(1 if data[i+1] > data[i]
                     else 0 for i in range(len(data)-1))
    print(f"part 1: {increments}")


with open('day1.txt') as reader:
    data = list(int(a) for a in reader.readlines())
    data = list(sum(data[i:i+3]) for i in range(len(data)-2))
    increments = sum(1 if data[i+1] > data[i]
                     else 0 for i in range(len(data)-1))
    print(f"part 2: {increments}")
