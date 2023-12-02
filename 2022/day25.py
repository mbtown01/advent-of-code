
snafuToDecDigitMap = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
decToSnafuDigitMap = {b: a for a, b in snafuToDecDigitMap.items()}


def snafuToDecimal(value: str):
    return sum(
        5**i * snafuToDecDigitMap[v]
        for i, v in enumerate(reversed(value))
    )


def decimalToSnafu(value: int):
    snafu = ''
    while value != 0:
        value, r = divmod(value, 5)
        if r == 3:
            value, r = value+1, '='
        elif r == 4:
            value, r = value+1, '-'
        snafu = f"{r}{snafu}"
    return snafu


def test():
    testValues = [
        ('1=-0-2', '1747'),
        ('12111', '906'),
        ('2=0=', '198'),
        ('21', '11'),
        ('2=01', '201'),
        ('111', '31'),
        ('20012', '1257'),
        ('112', '32'),
        ('1=-1=', '353'),
        ('1-12', '107'),
        ('12', '7'),
        ('1=', '3'),
        ('122', '37'),
    ]

    for snafu, decimal in testValues:
        test = snafuToDecimal(snafu)
        if test != int(decimal):
            raise RuntimeError(f"s2d {snafu}, {test} != {decimal}")

        test = decimalToSnafu(int(decimal))
        if test != snafu:
            raise RuntimeError(f"d2s {snafu}, {test} != {decimal}")


with open('2022/day25.txt') as reader:
    total = sum(snafuToDecimal(a.strip()) for a in reader)
    snafu = decimalToSnafu(total)
    print(total, snafu)
