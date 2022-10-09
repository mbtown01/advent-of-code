

with open('2020/day2.txt') as reader:
    inPolicyCountPt1, inPolicyCountPt2 = 0, 0
    for line in reader.readlines():
        line = line.strip()

        definition, password = line.split(': ')
        range, letter = definition.split(' ')
        range = list(int(a) for a in range.split('-'))
        occurrences = sum(1 if a == letter else 0 for a in password)

        inPolicyPt1 = (occurrences >= range[0]) and (occurrences <= range[1])
        if inPolicyPt1:
            inPolicyCountPt1 += 1

        isMatch = list(password[a-1] == letter for a in range)
        inPolicyPt2 = isMatch[0] != isMatch[1]
        if inPolicyPt2:
            inPolicyCountPt2 += 1

    print(f"inPolicyCountPt1={inPolicyCountPt1}")
    print(f"inPolicyCountPt2={inPolicyCountPt2}")
