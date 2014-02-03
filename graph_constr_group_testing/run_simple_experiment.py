import collections
import os
from graph_constr_group_testing import base_types, problem_json_io, problem_io


def sameSize(problemIterable):
    result = collections.defaultdict(list)
    for problem in problemIterable:
        result[problem.nodes_number()].append(problem)
    return result


def run_experiment(solverFactories, problemIterable, experimentStats):
    for solverFactory in solverFactories:
        for problem in problemIterable:
            statistics = base_types.TestStatistics()
            tester = base_types.PathTester(problem.faulty_set, statistics)
            solver = solverFactory(problem, tester, statistics)
            result = solver.solve()
            statistics.set_state(experimentStats.verify(result, problem.faulty_set))
            experimentStats.set_result(solver, problem, statistics)


def iterate_for_problems(directoryPath, decoder):
    dirpath = os.path.realpath(directoryPath)
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            yield decoder(filepath)
        except problem_io.NotGroupTestingDescriptionFile:
            pass


def run_experiment_for_json_directory(solverFactories, experimentStats, directoryPath):
    problemIterable = iterate_for_problems(directoryPath, problem_json_io.read_problem_from_file_of_name)
    return run_experiment(solverFactories, problemIterable, experimentStats)