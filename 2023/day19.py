import unittest
import numpy as np


class Implementation:

    oppositeInequalityMap = {'<': '>=', '>': '<='}

    def __init__(self, dataPath: str):
        self.workflowMap = dict()
        self.partList = list()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                line = line.strip()
                if line.startswith('{'):
                    self.partList.append(self._buildPart(line[1:-1]))
                elif len(line) > 0:
                    name, desc = line.strip().split('{')
                    self.workflowMap[name] = self._buildWorkflow(desc[:-1])

    def _buildWorkflow(self, desc: str):
        allRules, ruleList = desc.split(','), list()
        for rule in allRules[:-1]:
            comp, dest = rule.split(':')
            ruleList.append(dict(
                category=comp[0], inequality=comp[1],
                value=int(comp[2:]), dest=dest))
        return dict(ruleList=ruleList, default=allRules[-1])

    def _buildPart(self, desc: str):
        return {a.split('=')[0]: int(a.split('=')[1])
                for a in desc.split(',')}

    def _evalPartForWorkflow(self, part: dict, workflowName: dict):
        workflow = self.workflowMap[workflowName]
        for rule in workflow['ruleList']:
            ineq, cat, val = \
                rule['inequality'], rule['category'], rule['value']
            if ineq == '<' and part[cat] < val:
                return rule['dest']
            if ineq == '>' and part[cat] > val:
                return rule['dest']
        return workflow['default']

    def _findApprovedPaths(self,
                           workflowName: dict,
                           currentPath: list,
                           pathList: list):
        if workflowName == 'A':
            pathList.append(currentPath)
        elif workflowName != 'R':
            workflow = self.workflowMap[workflowName]
            inequalitiesList = list()
            for rule in workflow['ruleList']:
                localRule = rule.copy()
                localRule.pop('dest')
                self._findApprovedPaths(
                    rule['dest'], currentPath + inequalitiesList + [localRule], pathList)
                localRule = localRule.copy()
                localRule['inequality'] = \
                    self.oppositeInequalityMap[localRule['inequality']]
                inequalitiesList.append(localRule)
            self._findApprovedPaths(
                workflow['default'], currentPath + inequalitiesList, pathList)

    def _evalPathForPartCount(self, path: list):
        allValues = {a: np.ones((4000), dtype=np.int8) for a in 'xmas'}
        for rule in path:
            ineq, cat, val = \
                rule['inequality'], rule['category'], rule['value']
            if ineq == '<':
                allValues[cat][val-1:] = 0
            elif ineq == '<=':
                allValues[cat][val:] = 0
            elif ineq == '>':
                allValues[cat][:val] = 0
            elif ineq == '>=':
                allValues[cat][:val-1] = 0
            else:
                raise RuntimeError(f"Unknown inequality {ineq}")
        return np.prod(list(sum(a) for a in allValues.values()))

    def part1(self):
        result = 0
        for part in self.partList:
            workflowName = 'in'
            while workflowName not in ('A', 'R'):
                workflowName = self._evalPartForWorkflow(part, workflowName)
            if workflowName == 'A':
                result += sum(a for a in part.values())

        return result

    def part2(self):
        # I think this generally works, and our answer is in the range
        # of correct, but we're off somewhere.  Could be inequalities,
        # could be the rule chain logic is flawed...
        pathList = list()
        self._findApprovedPaths('in', list(), pathList)
        countList = list(self._evalPathForPartCount(path)
                         for path in pathList)
        return sum(countList)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 19114)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 373302)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 167409079868000)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 130262715574114)
