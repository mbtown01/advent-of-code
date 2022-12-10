

class Directory:

    def __init__(self, name: str, parentDir):
        self.name = name
        self.parentDir = parentDir
        self.subDirs = dict()
        self.fileSizes = dict()

    def findSize(self, atMost: int = 0, results: list = None):
        size = sum(a.findSize(atMost, results) for a in self.subDirs.values())
        size += sum(a for a in self.fileSizes.values())
        if size <= atMost and results is not None:
            results.append((self, size))
        return size


class TerminalParser:

    def __init__(self):
        self.rootDir = Directory('/', None)
        self.pwd = self.rootDir
        self.cmdMap = {'cd': self._cmd_cd, 'ls': self._cmd_ls}

    def _cmd_cd(self, dir: str, _: list):
        self.pwd = self.getDir(dir)
        if self.pwd is None:
            raise RuntimeError(f"Can't cd to '{dir}'")

    def _cmd_ls(self, outputLines: list):
        for line in outputLines:
            parts = line.split(' ')
            if parts[0] == 'dir':
                if parts[0] not in self.pwd.subDirs:
                    self.pwd.subDirs[parts[1]] = Directory(parts[1], self.pwd)
            else:
                self.pwd.fileSizes[parts[1]] = int(parts[0])

    def getDir(self, dir: str):
        pwd = self.pwd
        dirParts = dir.split('/')
        for i, dirPart in enumerate(dirParts):
            if dirPart == '' and i == 0:
                pwd = self.rootDir
            elif dirPart == '..':
                pwd = pwd.parentDir
            elif dirPart != '':
                pwd = pwd.subDirs.get(dirPart)
        return pwd

    def exec(self, allLines: list):
        allCmdsAndOutput = list()
        for i in range(len(allLines)):
            if allLines[i].startswith('$'):
                allCmdsAndOutput.append([allLines[i][2:]])
            else:
                allCmdsAndOutput[-1].append(allLines[i])

        for cmdAndOutput in allCmdsAndOutput:
            cmdParts = cmdAndOutput[0].split(' ')
            self.cmdMap[cmdParts[0]](*cmdParts[1:], cmdAndOutput[1:])


with open('2022/day7.txt') as reader:
    allLines = list(a.strip() for a in reader.readlines())

p = TerminalParser()
p.exec(allLines)
results = list()
size = p.getDir('/').findSize(100000, results)
part1 = sum(a[0].findSize() for a in results)
print(f"part 1: {part1}")

totalSpace, neededFreeSpace = 70000000, 30000000
size = p.getDir('/').findSize(totalSpace, results)
toRemove = neededFreeSpace - (totalSpace - size)
results = sorted(results, key=lambda a: a[1])
results = list(a for a in results if a[1] >= toRemove)

print(f"part 2: {results[0][1]}")
