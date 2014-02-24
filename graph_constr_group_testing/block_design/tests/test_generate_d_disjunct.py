from unittest import TestCase
from graph_constr_group_testing.block_design import generate_disjunct_from_hamming, check_is_d_disjunct

__author__ = 'bartek'


class TestGenerate_d_disjunct(TestCase):
    def test_generate_d_disjunct(self):
        m = generate_disjunct_from_hamming.generate_d_disjunct(14)
        self.assertTrue(m, check_is_d_disjunct.is_d_disjunct(m, 4))