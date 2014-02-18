from unittest import TestCase
import numpy
from graph_constr_group_testing.block_design import set_packing_design

__author__ = 'bartek'


class TestIs_d_disjunct(TestCase):
    def test_is_d_disjunct(self):
        m = set_packing_design.make_matrix([{0,1,2,3}, {0,1,4,5}, {0,2,4,6}], 7, 3)
        self.assertFalse(set_packing_design.is_d_disjunct(m, 1))
        m2 = set_packing_design.make_matrix([{0,1,3}, {0,2,4}, {1,2,5}, {3,4,5}], 6, 4)
        self.assertTrue(set_packing_design.is_d_disjunct(m2, 1))

    def test_column_contained(self):
        c = numpy.array([0,1,1,0]).reshape(4,1)
        c2 = numpy.array([1,1,1,1]).reshape(4,1)
        self.assertTrue(set_packing_design.contained_in(c, c2))

    def test_column_contained2(self):
        c = numpy.array([0,1,1,0]).reshape(4,1)
        c2 = numpy.array([1,0,1,1]).reshape(4,1)
        self.assertFalse(set_packing_design.contained_in(c, c2))
