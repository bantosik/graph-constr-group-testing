import collections
from graph_constr_group_testing.core import base_types


class SimpleExperimentStats(base_types.Verificator, base_types.ExperimentStatistics):
    def verify(self, result, faulty_set):
        return result == faulty_set

def averageQueriesForSize(results):
    result = []
    count = collections.defaultdict(int)
    sumallqueries = collections.defaultdict(int)
    for solver, problem, statistics in results:
        n = base_types.size_of_problem(problem)
        count[n] += 1
        sumallqueries[n] += statistics.get_var('all')

    for k, v in sumallqueries.iteritems():
        result.append((k, float(v)/count[k]))
    return zip(*sorted(result, key=lambda x: x[0]))


