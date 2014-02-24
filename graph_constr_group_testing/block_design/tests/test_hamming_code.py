import numpy
from graph_constr_group_testing.block_design import linear_codes, hamming_code

__author__ = 'bartek'



def test_hamming_matrix():
    assert (hamming_code.get_code(7) == linear_codes.Code(numpy.array([[ 1.,  1.,  0.,  1.,  0.,  0., 0.],
                                                      [ 1.,  0.,  1.,  0.,  1.,  0., 0.],
                                                      [ 0.,  1.,  1.,  0.,  0.,  1., 0.],
                                                      [ 1.,  1.,  1.,  0.,  0.,  0., 1.]]), 3))