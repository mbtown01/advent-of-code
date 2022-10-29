

class Group:

    def __init__(self):
        self.allQuestionsSet = set()
        self.sharedQuestionsSet = None

    def addRecordLine(self, line: str):
        for a in line:
            self.allQuestionsSet.add(a)
        if self.sharedQuestionsSet is None:
            self.sharedQuestionsSet = set(line)
        else:
            self.sharedQuestionsSet = \
                self.sharedQuestionsSet.intersection(line)


with open('2020/day6.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

groupList = [Group()]
for line in allLines:
    if len(line) > 0:
        groupList[-1].addRecordLine(line)
    else:
        groupList.append(Group())


all = sum(len(a.allQuestionsSet) for a in groupList)
print(f"Part 1: {all}")
shared = sum(len(a.sharedQuestionsSet) for a in groupList)
print(f"Part 2: {shared}")
