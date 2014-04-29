"""Module contains basic solver and statistic gathering utility classes"""

import collections
from graph_constr_group_testing import graph_utils
from graph_constr_group_testing.core import base_types


class IterativeSolver(base_types.GCGTSolver):
    def __init__(self, problem_description, tester):
        super(IterativeSolver, self).__init__(problem_description, tester)
        self.analysis_state = IterativeSolver.SimpleStateAnalyser(problem_description)

    def solve(self):
        iteration = 0
        try:
            while self.analysis_state.result_not_determined():
                path = self.path_generator.next()
                [result] = self.tester.test_paths([path])
                self.analysis_state.put_result(result, path)
                if self.stop(iteration, result, path):
                    raise StopIteration()
                iteration += 1
        except StopIteration:
            raise base_types.SolverError("Cannot generate new path, and result not yet determined")
        return self.analysis_state.get_positive_elements()

    class SimpleStateAnalyser(object):
        def __init__(self, problem_description):
            self.num_of_faulty_nodes = len(problem_description.faulty_set)
            self.nodes = collections.defaultdict(int)
            self.number_of_nodes_determined_as_faulty = len(problem_description.all_nodes)

            #all elements are guilty until proven innocent
            for i in problem_description.all_nodes:
                self.nodes[i] = True

        def put_result(self, result, elements):
            #element in path that gives negative result, will prove its innocence
            if not result:
                for e in elements:
                    if self.nodes[e]:
                        self.number_of_nodes_determined_as_faulty -=1
                    self.nodes[e] = False

        def result_not_determined(self):
            return self.number_of_nodes_determined_as_faulty > self.num_of_faulty_nodes

        def get_positive_elements(self):
            #remaining faulty element
            return set([e for e, state in self.nodes.iteritems() if state])



                
class BruteForceGCGTSolver(IterativeSolver):
    def __init__(self, problem_description, tester):
        super(BruteForceGCGTSolver, self).__init__(problem_description, tester)
        self.path_generator = graph_utils.generate_paths(self.graph, self.source, self.sink)



    def toDict(self):
        return {base_types.Solver.SOLVER_TYPE_TAG: 'bruteforce'}

    def stop(self, iteration, result, path):
        return False

class RandomSolver(IterativeSolver):
    def __init__(self, seed, maxiters, problem_description, tester):
        self.seed = seed
        self.maxiters = maxiters
        super(RandomSolver, self).__init__(problem_description, tester)
        self.path_generator = graph_utils.random_path_generator(self.graph, self.source, self.sink, seed)

    def stop(self, iteration, result, path):
        return iteration >= self.maxiters

    def toDict(self):
        return {base_types.Solver.SOLVER_TYPE_TAG: 'random', 'seed': self.seed, 'maxiters': self.maxiters}



        
            