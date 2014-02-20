from unittest import TestCase
from graph_constr_group_testing.block_design import check_is_d_disjunct, matrix_operations

__author__ = 'bartek'

is_d_disjunct_implementations = [check_is_d_disjunct.is_d_disjunct]


class suite(object):
    @staticmethod
    def is_1_disjunct(function):
        m = matrix_operations.NumpyMatrix.make_matrix([{0,1,2,3}, {0,1,4,5}, {0,2,4,6}])
        assert not function(m, 1)
    @staticmethod
    def is_not_1_disjunct(function):
        m2 = matrix_operations.NumpyMatrix.make_matrix([{0,1,3}, {0,2,4}, {1,2,5}, {3,4,5}])
        assert function(m2, 1)
    @staticmethod
    def is_1_disjunct2(function):
        sets = [{0,1}, {2,3}, {4,5}]
        matrix = matrix_operations.NumpyMatrix.make_matrix(sets).transpose()
        assert function(matrix, 1)
    @staticmethod
    def is_set_packing_graph_traversal(function):
        # this test checks if all paths from graph:
        # source -> {0, 1}
        # 0 -> {2}
        # 1 -> {2}
        # 2 -> {3, 4, 5}
        # 3 -> {6}
        # 4 -> {6}
        # 5 -> {6}
        sets = matrix_operations.NumpyMatrix.make_matrix(
            [{0,2,3,6}, {0,2,4,6}, {0,2,5,6}, {1, 2, 3, 6}, {1, 2, 4 ,6 }, {1, 2, 5, 6}]
        )
        assert not function(sets, 2)

def test_is_is_d_disjunct_generator():
    for attr in dir(suite):
        if attr.startswith('is_'):
            for impl in is_d_disjunct_implementations:
                yield getattr(suite, attr), impl

def test_is_2_set_packing():
    sets = [{0,1}, {2,3}, {4,5}]
    t = 2
    assert check_is_d_disjunct.is_packing_design(sets, t, 6)


class TestMatrix_operations(TestCase):
    def test_column_contained(self):
        c = matrix_operations.NumpyColumn.make_column_from_iter([0,1,1,0])
        c2 = matrix_operations.NumpyColumn.make_column_from_iter([1,1,1,1])
        self.assertTrue(c.contained_in(c2))

    def test_column_contained2(self):
        c = matrix_operations.NumpyColumn.make_column_from_iter([0,1,1,0])
        c2 = matrix_operations.NumpyColumn.make_column_from_iter([1,0,1,1])
        self.assertFalse(c.contained_in(c2))
