import unittest

import graph_constr_group_testing as gt_init
from graph_constr_group_testing import graph_constr_group_testing as gt

import networkx as nx

def graph_equal(g1, g2):
    return set(g1.edges_iter()) == set(g2.edges_iter())

class Test(unittest.TestCase):
    def setUp(self):
        self.problem1_graph =nx.DiGraph()
        self.problem1_graph.add_edge("START", "1")
        self.problem1_graph.add_edge("START", "2")
        self.problem1_graph.add_edge("1", "3")
        self.problem1_graph.add_edge("1", "4")
        self.problem1_graph.add_edge("2", "3")
        self.problem1_graph.add_edge("2", "4")
        self.problem1_graph.add_edge("3", "5")
        self.problem1_graph.add_edge("3", "6")
        self.problem1_graph.add_edge("4", "5")
        self.problem1_graph.add_edge("4", "6")
        self.problem1_graph.add_edge("5", "END")
        self.problem1_graph.add_edge("6", "END")
        

    def test_read_problem_from_file(self):
        g = gt.read_problem_from_file("test_data/test1.json")
        self.assertEquals(g.faulty_set, set(["1","3","5"]), "Faulty set read from problem description %s" % (g.faulty_set,))
        self.assertTrue(graph_equal(g.problem_graph.graph, self.problem1_graph), "should get right graph")
        self.assertEquals(g.problem_graph.source, "START", "Source should be START but is %s" % (g.problem_graph.source))
        self.assertEquals(g.problem_graph.sink, "START", "Source should be START but is %s" % (g.problem_graph.sink))
        