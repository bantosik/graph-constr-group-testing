"""Module contains basic solver and statistic gathering utility classes"""

import collections
from graph_constr_group_testing.core import base_types


class BruteForceGCGTSolver(base_types.GCGTSolver):
    def __init__(self, problem_description, tester):
        super(BruteForceGCGTSolver, self).__init__(problem_description, tester)
        self.analysis_state = BruteForceGCGTSolver.SimpleStateAnalyser(self.graph.nodes_iter())

    def solve(self):
        for path in generate_paths(self.graph, self.source, self.sink):
            [result] = self.tester.test_paths([path])
            self.analysis_state.put_result(result, path)
        return self.analysis_state.get_positive_elements()

    class SimpleStateAnalyser(object):
        def __init__(self, nodes_iterator):
            self.nodes = collections.defaultdict(int)
            #all elements are guilty until proven innocent
            for i in nodes_iterator:
                self.nodes[i] = True

        def put_result(self, result, elements):
            #element in path that gives negative result, will prove its innocence
            if not result:
                for e in elements:
                    self.nodes[e] = result

        def get_positive_elements(self):
            #remaining faulty element
            return set([e for e, state in self.nodes.iteritems() if state])
                
def generate_paths(graph, start_point, end_point):
    if start_point == end_point:
        yield [end_point]
    else:
        for begin, end in graph.out_edges(start_point):
            for p in generate_paths(graph, end, end_point):
                yield [begin] + p
        

    

    
        
            