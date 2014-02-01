"""Module contains basic solver and statistic gathering utility classes"""

import collections

Problem = collections.namedtuple("Problem", ["problem_graph", "faulty_set", "description"])
ProblemGraph = collections.namedtuple("ProblemGraph", ["graph", "source", "sink"])

class BruteForceSolver(object):
    def __init__(self, problem_description):
        """
        :type problem_description: Problem
        """
        self.problem_description = problem_description
        self.graph = self.problem_description.problem_graph.graph
        self.source = self.problem_description.problem_graph.source
        self.sink = self.problem_description.problem_graph.sink

        self.statistics = TestStatistics()
        self.analysis_state = BruteForceSolver.SimpleStateAnalyser(self.graph.nodes_iter())
        self.tester = PathTester(problem_description.faulty_set, self.statistics)


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
        
class PathTester(object):
    def __init__(self, faulty_set, stats):
        self.faulty_set = faulty_set
        self.stats = stats

    def test_path(self, path):
        result = any((x in self.faulty_set) for x in path)
        if result:
            self.stats.inc_positive_query()
        else:
            self.stats.inc_negative_query()
        return result


class TestStatistics(object):
    def __init__(self):
        self.number_of_runs = 0
        self.positive_queries = 0
        self.negative_queries = 0
    
    def end_run(self):
        self.number_of_runs = self.number_of_runs + 1
        
    def get_all_queries(self):
        return self.positive_queries + self.negative_queries

    def inc_positive_query(self):
        self.positive_queries += 1

    def inc_negative_query(self):
        self.negative_queries += 1

    def get_negative_queries(self):
        return self.negative_queries
    
    def get_positive_queries(self):
        return self.positive_queries
    
    def get_number_of_runs(self):
        return self.number_of_runs
    

    
        
            