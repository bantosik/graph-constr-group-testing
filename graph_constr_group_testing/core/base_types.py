"""
Contains base data structures for defining graph constrained group testing problem,
and interfaces to operate on them.

Basic structure to exchange graph constrained group testing problem definition is :class:`Problem`.
It consists of enumeration of faulty elements, graph of links between elements and natural language
description of the problem. Graph is described by :class:`ProblemGraph` which consists of
:class:`networkx.DiGraph`, and distinguished nodes stored in :attr:`ProblemGraph.source`,
and :attr:`ProblemGraph.sink`

Interface of every algorithm solving group constrained group testing problem is defined by
:class:`Solver`, Abstract class :class:`ExperimentStatistics` defines generic interface that can
be used by experiment runners to verify result returned by solver. Result later is stored together
with statistics (:class:`TestStatistics`) in memory, where it can be retrieved for each problem/solver pair.

Experiment runner is a function accepting :class:`Experiment` parameter that fills it during call.
"""

import collections
from abc import ABCMeta, abstractmethod


class ToDict(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def toDict(self):
        raise NotImplementedError()

class EmptyToDict(ToDict):
    def toDict(self):
        return {}

class Problem(collections.namedtuple("Problem", ["all_nodes", "faulty_set", "description"]), EmptyToDict):
    pass

class GCGTProblem(collections.namedtuple("GCGTProblem", ["all_nodes", "faulty_set", "description", "problem_graph"]), EmptyToDict):
    pass

ProblemGraph = collections.namedtuple("ProblemGraph", ["graph", "source", "sink"])



class ExperimentStatistics(object):
    """
    Maintains statistics related with the experiment, for each problem and solver statistics object is gathered
    """

    def __init__(self, rendererMapping):
        self._renderers = rendererMapping or {}
        for k, v in self._renderers.iteritems():
            if v is None:
                self._renderers[k] = lambda x: x.toDict()

        self.results = []
        self.headers = set({})

    def set_result(self, objectsMapping):
        result = {}
        for k, v in objectsMapping.iteritems():
            rendered = self._render(k, v)

            self._add_headers(rendered)
            result.update(rendered)
        self.results.append(result)

    def _add_headers(self, rendered):
        for k in rendered:
            self.headers.add(k)

    def _render(self, rendererIdentifier, obj):
        result = {}
        if isinstance(obj, (int, float, str)):
            defaultrenderer = lambda x: {'value': x}
        else:
            defaultrenderer = lambda obj: obj.toDict()
        renderer = self._renderers.get(rendererIdentifier, defaultrenderer)
        for k, v in renderer(obj).iteritems():
            result[self._join(rendererIdentifier, k)] = v
        return result

    def _join(self, *args):
        return ".".join(args)

    def process(self):
        raise NotImplementedError()

class TestStatistics(ToDict):
    """
    Maintains various statistics related with the single run of group testing algorithm
    """
    def __init__(self):
        self.variable_dict = {}

    def set_var(self, var, value):
        self.variable_dict[var] = value

    def get_var(self, var):
        return self.variable_dict[var]

    def inc_var(self, var):
        self.variable_dict[var] = self.variable_dict.get(var, 0) + 1

    def toDict(self):
        return self.variable_dict


class Solver(ToDict):
    SOLVER_TYPE_TAG = 'solver_type'

    def __init__(self, problem_description, tester, *args, **kwargs):
        raise NotImplementedError()

    def solve(self):
        """
        runs algorithm solving graph constrained group testing problem

        :returns: set of nodes identified by algorithm as positive
        :rtype: set
        """
        raise NotImplementedError()

class SolverError(Exception):
    pass

class GCGTSolver(Solver):
    """
    Interface of classes implementing combinatorial group testing algorithm.

    Problem description and tester object have to be inserted in constructor
    """

    def __init__(self, problem_description, tester, *args, **kwargs):
        """
        :param problem_description: graph constrained combinatorial problem description
        :type problem_description: base_types.Problem
        :param tester: tester object which will test all paths
        :type tester: base_types.PathTester
        """
        self.problem_description = problem_description
        self.graph = self.problem_description.problem_graph.graph
        self.source = self.problem_description.problem_graph.source
        self.sink = self.problem_description.problem_graph.sink
        self.tester = tester



class SetTester(object):
    def test_paths(self, paths):
        """
        check results for batch tests of paths

        :param paths: paths that will be tested
        :type paths: list[set]
        :returns: list of boolean representing results for each of the `paths`.
        :rtype: list[bool]
        """
        raise NotImplementedError()
