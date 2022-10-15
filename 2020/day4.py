import re

with open('2020/day4.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())


class BadPassportError(RuntimeError):
    pass


class Validator:

    def __init__(self):
        self.hgtRegex = re.compile('[a-z0-9]')
        self.pidRegex = re.compile('[0-9]')

    def validateNumeric(self, value: str, low: int, high: int):
        if int(value) < low or int(value) > high:
            raise BadPassportError(
                f"Value {value} not between {low} and {high}")

    def validateInList(self, value: str, acceptables: list):
        if value not in acceptables:
            raise BadPassportError(f"Value '{value}' not in {acceptables}")

    def validateHgt(self, value: str):
        measurement, units = value[:-2], value[-2:]
        self.validateInList(units, ['cm', 'in'])
        if units == 'cm':
            self.validateNumeric(measurement, 150, 193)
        else:
            self.validateNumeric(measurement, 59, 76)

    def validateHcl(self, value: str):
        if len(value) != 7 or value[0] != '#':
            raise BadPassportError('Bad length or starting char')
        for char in value[1:]:
            if self.hgtRegex.match(char) is None:
                raise BadPassportError('Bad content char')

    def validateEcl(self, value: str):
        self.validateInList(
            value, ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

    def validatePid(self, value: str):
        if len(value) != 9:
            raise BadPassportError('Bad length')
        for char in value:
            if self.pidRegex.match(char) is None:
                raise BadPassportError('Bad content char')


class Passport:
    allFields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

    def __init__(self, text: str):
        self.keyValues = dict()
        fieldsNotSeen = dict.fromkeys(Passport.allFields)
        for keyValuePair in text.split(' '):
            key, value = keyValuePair.split(':')
            self.keyValues[key] = value
            if key not in Passport.allFields:
                raise BadPassportError()
            del fieldsNotSeen[key]

        if len(fieldsNotSeen) != 0:
            if len(fieldsNotSeen) != 1 or 'cid' not in fieldsNotSeen:
                raise BadPassportError()

    def validate(self, validator: Validator):
        validator.validateNumeric(self.keyValues['byr'], 1920, 2002)
        validator.validateNumeric(self.keyValues['iyr'], 2010, 2020)
        validator.validateNumeric(self.keyValues['eyr'], 2020, 2030)
        validator.validateHgt(self.keyValues['hgt'])
        validator.validateHcl(self.keyValues['hcl'])
        validator.validateEcl(self.keyValues['ecl'])
        validator.validatePid(self.keyValues['pid'])


validator = Validator()
validCount1, validCount2, startIndex = 0, 0, 0
for index, line in enumerate(allLines):
    if len(line) == 0 or index == len(allLines)-1:
        passportText = ' '.join(allLines[startIndex:index])
        startIndex = index+1
        try:
            passport = Passport(passportText)
            validCount1 += 1
            passport.validate(validator)
            validCount2 += 1
        except BadPassportError as ex:
            pass

print(f"Valid passports: {validCount1}")
print(f"Valid passport contents: {validCount2}")
