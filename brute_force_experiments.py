import collections
from graph_constr_group_testing import run_simple_experiment, brute_force_solver, interface, base_types


class SimpleExperimentStats(interface.ExperimentStatistics):
    def verify(self, result, faulty_set):
        return result == faulty_set

def averageQueriesForSize(results):
    result = []
    count = collections.defaultdict(int)
    sumallqueries = collections.defaultdict(int)
    for solver, problem, statistics in results:
        n = base_types.size_of_problem(problem)
        count[n] += 1
        sumallqueries[n] += statistics.get_all_queries()

    for k, v in sumallqueries.iteritems():
        result.append((k, float(v)/count[k]))
    return zip(*sorted(result, key=lambda x: x[0]))


bruteForceFactory = brute_force_solver.BruteForceSolver
experimentStats = SimpleExperimentStats()

run_simple_experiment.run_experiment_for_json_directory([bruteForceFactory], experimentStats, directoryPath='test_data/experiment1')
