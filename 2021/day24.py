from collections import defaultdict

from numpy import iterable, var


class Statement:

    def __init__(self, op: callable, args: list, line: str):
        self.op = op
        self.args = args
        self.line = line
        self.parent = None

    def __repr__(self) -> str:
        return f"[Statement '{self.line}']"

    def exec(self):
        self.op(*self.args)


class Program:

    def __init__(self, statements: list) -> None:
        self.input = list()
        self.state = defaultdict(int)
        self.varList = ['w', 'x', 'y', 'z']
        self._compiled = list()

        varLastStatement = dict()
        for statement in statements:
            statement = statement.strip()
            tokens = statement.split()
            args = list(a if a in self.varList else int(a) for a in tokens[1:])
            op = tokens[0]
            if 'inp' == op:
                assert 1 == len(args)
                statement = Statement(self.opInp, args, statement)
                if args[0] in varLastStatement:
                    del varLastStatement[args[0]]
            elif 'add' == op:
                assert 2 == len(args)
                statement = Statement(self.opAdd, args, statement)
            elif 'mul' == op:
                assert 2 == len(args)
                statement = Statement(self.opMul, args, statement)
                if '0' == args[1] and args[0] in varLastStatement:
                    del varLastStatement[args[0]]
            elif 'div' == op:
                assert 2 == len(args)
                statement = Statement(self.opDiv, args, statement)
            elif 'mod' == op:
                assert 2 == len(args)
                statement = Statement(self.opMod, args, statement)
            elif 'eql' == op:
                assert 2 == len(args)
                statement = Statement(self.opEql, args, statement)
            else:
                raise RuntimeError(f"{op} is not a recognized operation")

            statement.parent = varLastStatement.get(args[0])
            varLastStatement[args[0]] = statement
            self._compiled.append(statement)

    def opInp(self, a: str):
        self.state[a] = self.input.pop(0)
        print(self.state)

    def opAdd(self, a: str, b: object):
        self.state[a] = self.state[a] + self.state.get(b, b)

    def opMul(self, a: str, b: object):
        self.state[a] = self.state[a] * self.state.get(b, b)

    def opDiv(self, a: str, b: object):
        self.state[a] = self.state[a] // self.state.get(b, b)

    def opMod(self, a: str, b: object):
        self.state[a] = self.state[a] % self.state.get(b, b)

    def opEql(self, a: str, b: object):
        self.state[a] = 1 if self.state[a] == self.state.get(b, b) else 0

    def exec(self, input: iterable):
        self.input = list(int(a) for a in input)
        assert(14 == len(self.input))
        self.state = dict()
        for a in self.varList:
            self.state[a] = 0

        for statement in self._compiled:
            statement.exec()

        print(self.state)

    def analyze(self, input: iterable):
        self.input = list(int(a) for a in input)
        assert(14 == len(self.input))

        allVariables = list()
        for i in range(18):
            uniqueParams = set()
            allParams = list()
            firstStatement = self._compiled[i]
            for d in range(14):
                thisStatement = self._compiled[d*18+i]
                if len(thisStatement.args) == 2:
                    allParams.append(thisStatement.args[1])
                    if thisStatement.args[1] != firstStatement.args[1]:
                        uniqueParams.add(firstStatement.args[1])
                        uniqueParams.add(thisStatement.args[1])

            if len(uniqueParams) > 0:
                allVariables.append(allParams)

        allTuples = list(zip(*allVariables))
        for t in allTuples:
            print(t)

        """
        Any tuple that has (b < 0) MUST have x == w as there are
        zeven tuples that do and do NOT.  With multiplication and
        integer division this gets z starting at zero and BACK to
        zero.  
        """

        def algo(input: list):
            w, x, z = (0, 0, 0)
            for i, (a, b, c) in enumerate(allTuples):
                w = input[i]
                x = z % 26 + b
                z = z // a
                if x != w:
                    z = 26*z + w + c
                print(w, x, z, b < 0)
            return z

        return algo(list(int(a) for a in input))


with open('2021/day24.txt') as reader:
    program = Program(reader.readlines())
    # program.analyze('91398299697996')
    print()
    # comments for  '12334556776421'
    # program.analyze('91398299697996')
    program.analyze('41171183141291')
