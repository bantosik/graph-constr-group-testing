from graph_constr_group_testing.block_design import recovery, generate_disjunct_from_hamming, matrix_operations
from graph_constr_group_testing.core import base_types

__author__ = 'bartek'


def map_with_assignment(blocks, assignment):
    for block in blocks:
        yield (assignment[b] for b in block)


def run_tests_according_to_matrix(disjunct_matrix, assignment, tester):
    result = tester.test_paths(map_with_assignment(disjunct_matrix.get_blocks(), assignment))
    return matrix_operations.NumpyColumn.make_column_from_iter(result)

class HammingGroupTestingSolver(base_types.Solver):
    def __init__(self, problem, tester, *args, **kwargs):
        self.all_nodes = problem.all_nodes
        self.faulty_set = problem.faulty_set
        self.tester = tester
        
    def solve(self):
        size = len(self.all_nodes)
        assignment = list(self.all_nodes)
        disjunct_matrix = generate_disjunct_from_hamming.generate_d_disjunct(size)
        result_column = run_tests_according_to_matrix(disjunct_matrix, assignment, self.tester)
        row = recovery.recover_from_disjunct(disjunct_matrix, result_column, 2)
        return {assignment[index] for index in row}

    def toDict(self):
        return {base_types.Solver.SOLVER_TYPE_TAG: 'hammingsolver'}
