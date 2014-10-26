from functools import partial
from graph_constr_group_testing import iterative_solvers, runners, results_analyser
from graph_constr_group_testing.core import features

number_of_random_solvers = 10
maxiters = 10000

randomSolvers = [partial(iterative_solvers.RandomSolver, i, maxiters) for i in xrange(number_of_random_solvers)]
solverFactories = [iterative_solvers.BruteForceGCGTSolver] + randomSolvers

featuresRenderers = {runners.PROBLEM_TAG: features.size_of_problem,
                     runners.PROBLEM_ID_TAG: partial(features.id, runners.PROBLEM_ID_TAG)}

csvStats = results_analyser.CsvStats('results.csv', featuresRenderers)
runners.run_experiment_for_json_directory(solverFactories,
                                          csvStats,
                                          'test_data/small_size_large_instances')

csvStats.process()

