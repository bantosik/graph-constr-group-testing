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

Problem = collections.namedtuple("Problem", ["problem_graph", "faulty_set", "description"])
ProblemGraph = collections.namedtuple("ProblemGraph", ["graph", "source", "sink"])

def size_of_problem(problem):
    return problem.problem_graph.graph.number_of_nodes() - 2


from abc import abstractmethod, ABCMeta


class ExperimentStatistics(object):
    """
    Maintains statistics related with the experiment, for each problem and solver statistics object is gathered
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.results = []

    @abstractmethod
    def verify(self, result, faulty_set):
        raise NotImplementedError()

    def set_result(self, solver, problem, statistics):
        self.results.append((solver, problem, statistics))


class TestStatistics(object):
    """
    Maintains various statistics related with the single run of group testing algorithm
    """
    def __init__(self):
        self.number_of_runs = 0
        self.positive_queries = 0
        self.negative_queries = 0

    def end_run(self):
        """
        called when a batch of paths is inserted to testing system :class:``
        """
        self.number_of_runs = self.number_of_runs + 1

    def get_all_queries(self):
        """
        check number of all queries (paths)
        """
        return self.positive_queries + self.negative_queries

    def inc_positive_query(self):
        """
        called when a query returns positive result
        """
        self.positive_queries += 1

    def inc_negative_query(self):
        """
        called when a query returns negative result
        """
        self.negative_queries += 1

    def get_negative_queries(self):
        return self.negative_queries

    def get_positive_queries(self):
        return self.positive_queries

    def get_number_of_runs(self):
        return self.number_of_runs

    def set_state(self, state):
        self.state = state


class GCGTSolver(object):
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

    def solve(self):
        """
        runs algorithm solving graph constrained group testing problem

        :returns: set of nodes identified by algorithm as positive
        :rtype: set
        """
        raise NotImplementedError()


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