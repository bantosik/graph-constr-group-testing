import collections
import os
from graph_constr_group_testing import verificators
from graph_constr_group_testing.core import base_types, non_overlapping_set_tester
from graph_constr_group_testing.io import problem_io, problem_json_io


SOLVER_TAG = 'solver'
PROBLEM_TAG = 'problem'
STATISTICS_TAG = 'statistics'
PROBLEM_ID_TAG = 'problem_id_tag'

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
    listOfProblems = list(problemIterable)
    for solverFactory in solverFactories:
        problemId = 0
        for problem in listOfProblems:
            statistics = base_types.TestStatistics()
            tester = non_overlapping_set_tester.NonOverlappingSetTester(problem.faulty_set, statistics)
            solver = solverFactory(problem, tester)
            try:
                result = verificators.verify(solver.solve(), problem.faulty_set)
            except base_types.SolverError:
                result = "ERROR"
            statistics.set_var('result', result)
            experimentStats.set_result({SOLVER_TAG: solver, PROBLEM_TAG: problem, STATISTICS_TAG: statistics, PROBLEM_ID_TAG: problemId})
            problemId += 1

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