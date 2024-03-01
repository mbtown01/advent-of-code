import unittest
from math import lcm


class RuntimeContext:

    def __init__(self):
        self.eventQueue = list()
        self.pulseCountMap = {False: 0, True: 0}
        self.pumpCount = 0

    def pulse(self, srcModule, destModule, value):
        self.pulseCountMap[value] += 1
        self._enqeue(destModule.pulse, srcModule, value, self)

    def _enqeue(self, method, *args, **kwargs):
        self.eventQueue.append((method, args, kwargs))

    def pump(self):
        while len(self.eventQueue) > 0:
            method, args, kwargs = self.eventQueue.pop(0)
            method(*args, **kwargs)
        self.pumpCount += 1


class Module:

    def __init__(self, name: str, *, defaultPulse: bool = None):
        self.name = name
        self.defaultPulse = defaultPulse
        self.outputModuleList = list()
        self.inputModuleList = list()
        self.listenerList = list()

    def __repr__(self) -> str:
        return f"[{type(self).__name__} '{self.name}']"

    def pulse(self, srcModule, value: bool, runtimeContext: RuntimeContext):
        output = self._pulse(srcModule, value)
        for listener in self.listenerList:
            listener(self, value)
        if output is not None:
            for module in self.outputModuleList:
                runtimeContext.pulse(self, module, output)

    def _pulse(self, srcModule, value: bool):
        return self.defaultPulse


class FlipFlopModule(Module):
    # HIGH inputs ignore, low inputs toggles the current state and then
    # sends the result forward to all outputs

    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def _pulse(self, srcModule, value: bool):
        if not value:
            self.state = not self.state
            return self.state
        return None


class ConjunctionModule(Module):
    # Returns LOW if ALL the last-received pulses from inputs were
    # HIGH, otherwise returns HIGH (it's a NAND gate)

    def __init__(self, name: str):
        super().__init__(name)
        self.inputMap = dict()

    def _pulse(self, srcModule, value: bool):
        self.inputMap[srcModule] = value
        return not all(self.inputMap.get(a, False)
                       for a in self.inputModuleList)


class Implementation:

    def __init__(self, dataPath: str):
        self.moduleMap, moduleOutputsMap = dict(), dict()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                name, outputs = line.strip().split(' -> ')
                if name.startswith('&'):
                    module = ConjunctionModule(name[1:])
                elif name.startswith('%'):
                    module = FlipFlopModule(name[1:])
                elif name == 'broadcaster':
                    module = Module(name, defaultPulse=False)
                else:
                    raise RuntimeError(f"Unrecognized module name '{name}'")
                self.moduleMap[module.name] = module
                moduleOutputsMap[module.name] = outputs

            for name, outputs in moduleOutputsMap.items():
                for outputName in outputs.split(', '):
                    if outputName not in self.moduleMap:
                        self.moduleMap[outputName] = Module(outputName)
                    self.moduleMap[name].outputModuleList.append(
                        self.moduleMap[outputName])
                    self.moduleMap[outputName].inputModuleList.append(
                        self.moduleMap[name])

    def emitGraph(self, path: str):
        # checkout https://edotor.net/
        with open(path, "w", encoding="utf8") as file:
            print("digraph {", file=file)
            for name, module in self.moduleMap.items():
                if len(module.outputModuleList) > 0:
                    group = " ".join(a.name for a in module.outputModuleList)
                    print(f"    {name} -> {{{group}}};", file=file)

            for name, module in self.moduleMap.items():
                if isinstance(module, FlipFlopModule):
                    print(f"    {name} [shape=box, color=blue];", file=file)
                elif isinstance(module, ConjunctionModule):
                    print(f"    {name} [shape=oval, color=green];", file=file)
                else:
                    print(f"    {name} [shape=diamond, color=red];", file=file)
            print("}", file=file)

    def part1(self):
        runtimeContext = RuntimeContext()
        for _ in range(1000):
            runtimeContext.pulse(None, self.moduleMap['broadcaster'], False)
            runtimeContext.pump()
        return runtimeContext.pulseCountMap[False] * \
            runtimeContext.pulseCountMap[True]

    def part2(self):
        runtimeContext = RuntimeContext()
        moduleResultMap = dict()

        def hfInputListener(module: Module, value: bool):
            if not value and module not in moduleResultMap:
                moduleResultMap[module] = runtimeContext.pumpCount + 1

        # When you look at the large graph, it's 4 independent adder circuits,
        # which all ultimately feed into the 'hf' NAND/Conjunction module.
        # What we're doing here is figuring out how many event loop pumps it
        # takes to get each adder circuit to pulse LOW into hf.  We then
        # know it's the least common mulutiple of pumps...
        hfModule = self.moduleMap['hf']
        for module in hfModule.inputModuleList:
            module.listenerList.append(hfInputListener)
        while len(moduleResultMap) != len(hfModule.inputModuleList):
            runtimeContext.pulse(None, self.moduleMap['broadcaster'], False)
            runtimeContext.pump()

        return lcm(*moduleResultMap.values())


class TestCase(unittest.TestCase):

    def test_part1_ex1(self):
        impl = Implementation(f'2023/data/{__name__}_example1.txt')
        result = impl.part1()
        self.assertEqual(result, 32000000)

    def test_part1_ex2(self):
        impl = Implementation(f'2023/data/{__name__}_example2.txt')
        result = impl.part1()
        self.assertEqual(result, 11687500)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 807069600)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 221453937522197)
