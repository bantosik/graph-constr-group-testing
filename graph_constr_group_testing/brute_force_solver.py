"""Module contains basic solver and statistic gathering utility classes"""

import collections
from graph_constr_group_testing import base_types


class BruteForceSolver(object):
    def __init__(self, problem_description):
        """
        :type problem_description: Problem
        """
        self.problem_description = problem_description
        self.graph = self.problem_description.problem_graph.graph
        self.source = self.problem_description.problem_graph.source
        self.sink = self.problem_description.problem_graph.sink

        self.statistics = base_types.TestStatistics()
        self.analysis_state = BruteForceSolver.SimpleStateAnalyser(self.graph.nodes_iter())
        self.tester = base_types.PathTester(problem_description.faulty_set, self.statistics)


    def solve(self):
        for path in generate_paths(self.graph, self.source, self.sink):
            result = self.tester.test_path(path)
            self.statistics.end_run()
            self.analysis_state.put_result(result, path)
        return self.analysis_state.get_positive_elements(), self.statistics

    class SimpleStateAnalyser(object):
        def __init__(self, nodes_iterator):
            self.nodes = collections.defaultdict(int)
            for i in nodes_iterator:
                self.nodes[i] = False

        def put_result(self, result, elements):
            for e in elements:
                self.nodes[e] = result

        def get_positive_elements(self):
            return set([e for e, state in self.nodes.iteritems() if state])
                
def generate_paths(graph, start_point, end_point):
    if start_point == end_point:
        yield []
    else:
        for begin, end in graph.out_edges(start_point):
            for p in generate_paths(graph, end, end_point):
                yield [begin] + p
        

    

    
        
            