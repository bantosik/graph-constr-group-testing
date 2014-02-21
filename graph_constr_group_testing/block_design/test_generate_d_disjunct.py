import numpy

__author__ = 'bartek'

from generate_d_disjunct import generate_hamming_matrix


def test_hamming_matrix():
    assert (generate_hamming_matrix(7) == numpy.array([[ 1.,  1.,  0.,  1.,  0.,  0., 0.],
                                                      [ 1.,  0.,  1.,  0.,  1.,  0., 0.],
                                                      [ 0.,  1.,  1.,  0.,  0.,  1., 0.],
                                                      [ 1.,  1.,  1.,  0.,  0.,  0., 1.]])).all()