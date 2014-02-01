import collections

__author__ = 'bartek'


Problem = collections.namedtuple("Problem", ["problem_graph", "faulty_set", "description"])
ProblemGraph = collections.namedtuple("ProblemGraph", ["graph", "source", "sink"])

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