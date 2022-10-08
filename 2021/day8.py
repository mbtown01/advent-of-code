from typing import DefaultDict
import numpy as np

"""
 aaaa            aaaa    aaaa        
b    c       c       c       c  b    c
b    c       c       c       c  b    c
                 dddd    dddd    dddd
e    f       f  e            f       f
e    f       f  e            f       f
 gggg            gggg    gggg        

 aaaa    aaaa    aaaa    aaaa    aaaa
b       b            c  b    c  b    c
b       b            c  b    c  b    c
 dddd    dddd            dddd    dddd
     f  e    f       f  e    f       f
     f  e    f       f  e    f       f
 gggg    gggg            gggg    gggg
 """

KNOWN_LENGTHS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}

KNOWN_DIGITS = {
    0: 'abc efg',  # 6 last remaining 6 (F)
    1: '  c  f ',  # 2 KNOWN
    2: 'a cde g',  # 5, last remaining 5 (D)
    3: 'a cd fg',  # 5, only 5 fully containing 1 (A)
    4: ' bcd f ',  # 4 KNOWN
    5: 'ab d fg',  # 5, only 5 that is subset of 6 (C)
    6: 'ab defg',  # 6, only 6 NOT fully containing 1 (B)
    7: 'a c  f ',  # 3 KNOWN
    8: 'abcdefg',  # 7 KNOWN
    9: 'abcd fg',  # 6, only 6 fully containing 5 (E)
}


def containsSignal(text: str, substr: str):
    for a in substr:
        if a not in text:
            return False

    return True


def sortSignal(signal: str):
    return ''.join(sorted(a for a in signal))


def findSignal(signals: list, data: list):
    assert len(data) == 1
    signals.remove(data[0])
    return data[0]


with open('day8.txt') as reader:
    outputSum, knownNumCounts = 0, 0

    for line in reader.readlines():
        signals, outputs = line.strip().split('|')
        outputs = list(sortSignal(a) for a in outputs.strip().split(' '))
        knownNumCounts += sum(
            1 if len(a) in KNOWN_LENGTHS else 0 for a in outputs)

        signals = list(sortSignal(a) for a in signals.strip().split(' '))
        digitMap = dict()
        for signal in signals.copy():
            digit = KNOWN_LENGTHS.get(len(signal))
            if digit is not None:
                digitMap[digit] = signal
                signals.remove(signal)

        # 5 is the only len(5) that contains 1
        digitMap[3] = findSignal(signals, list(
            a for a in signals if len(a) == 5 and
            containsSignal(a, digitMap[1])))
        digitMap[6] = findSignal(signals, list(
            a for a in signals if len(a) == 6 and
            not containsSignal(a, digitMap[1])))
        digitMap[5] = findSignal(signals, list(
            a for a in signals if len(a) == 5 and
            containsSignal(digitMap[6], a)))
        digitMap[2] = findSignal(signals, list(
            a for a in signals if len(a) == 5))
        digitMap[9] = findSignal(signals, list(
            a for a in signals if len(a) == 6 and
            containsSignal(a, digitMap[5])))
        digitMap[0] = findSignal(signals, list(
            a for a in signals if len(a) == 6))

        signalMap = {b: a for a, b in digitMap.items()}
        value = int(''.join(list(str(signalMap[a]) for a in outputs)))
        outputSum += value

    print(f"part 1: unique counts = {knownNumCounts}")
    print(f"part 2: outputSum={outputSum}")
