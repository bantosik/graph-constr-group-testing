import unittest

import graph_constr_group_testing as gt_init
from graph_constr_group_testing import problem_json_io as problem_io
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
        g = problem_io.read_problem_from_file("test_data/test1.json")
        self.assertEquals(g.faulty_set, set(["1","3","5"]), "Faulty set read from problem description %s" % (g.faulty_set,))
        self.assertTrue(graph_equal(g.problem_graph.graph, self.problem1_graph), "should get right graph")
        self.assertEquals(g.problem_graph.source, "START", "Source should be START but is %s" % (g.problem_graph.source))
        self.assertEquals(g.problem_graph.sink, "END", "Source should be START but is %s" % (g.problem_graph.sink))
        
    def test_path_tester(self):
        g = problem_io.read_problem_from_file("test_data/test1.json")
        path_tester = gt.PathTester(g.faulty_set)
        p1 = ["2","4","6"]
        p2 = ["1","4","6"]
        p3 = ["2","3","6"]
        result = path_tester.test_path(p1)
        self.assertFalse(result, "For %s path test1 should give negative result" % (p1,))
        result = path_tester.test_path(p2)
        self.assertTrue(result, "For %s path test1 should give positive result" % (p2,))
        result = path_tester.test_path(p3)
        self.assertTrue(result, "For %s path test1 should give positive result" % (p3,))
        self.assertEquals(path_tester.get_positive_queries(), 2, "Should be two positive queries got %d" % (path_tester.get_positive_queries(),))
        self.assertEquals(path_tester.get_negative_queries(), 1, "Should be one negative queries got %d" % (path_tester.get_negative_queries(),))
        self.assertEquals(path_tester.get_all_queries(), 3, "Should be 3 queries in total got %d" % (path_tester.get_all_queries(),))
        