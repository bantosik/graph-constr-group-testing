import numpy
from graph_constr_group_testing.block_design import linear_codes

__author__ = 'bartek'

from hamming_code import get_code


def test_hamming_matrix():
    assert (get_code(7) == linear_codes.Code(numpy.array([[ 1.,  1.,  0.,  1.,  0.,  0., 0.],
                                                      [ 1.,  0.,  1.,  0.,  1.,  0., 0.],
                                                      [ 0.,  1.,  1.,  0.,  0.,  1., 0.],
                                                      [ 1.,  1.,  1.,  0.,  0.,  0., 1.]]), 3))