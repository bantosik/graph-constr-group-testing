import collections
import os
from graph_constr_group_testing.core import base_types, non_overlapping_set_tester
from graph_constr_group_testing.io import problem_io, problem_json_io


def sameSize(problemIterable):
    result = collections.defaultdict(list)
    for problem in problemIterable:
        result[problem.nodes_number()].append(problem)
    return result


def run_experiment(solverFactories, problemIterable, experimentStats):
    """
    Function running each of solvers created by solverFactories for every problem from problemIterable
    storing corresponding statistics into experimentStats

    :param solverFactories: list of functions creating different solvers (or different configured solvers)
    :type solverFactories: (base_types.Problem, base_types.SetTester, base_types.TestStatistics) -> base_types.GCGTSolver
    :param problemIterable: iterable of problems for which each of the solver has to examined
    :type problemIterable: list[base_types.Problem]
    :param experimentStats: object storing results for each pair solver, problem
    :type :
    """
    for solverFactory in solverFactories:
        for problem in problemIterable:
            statistics = base_types.TestStatistics()
            tester = non_overlapping_set_tester.NonOverlappingSetTester(problem.faulty_set, statistics)
            solver = solverFactory(problem, tester)
            result = solver.solve()
            statistics.set_var('result', experimentStats.verify(result, problem.faulty_set))
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