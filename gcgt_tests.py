import StringIO
import unittest

import networkx as nx

from graph_constr_group_testing import problem_json_io as problem_io, base_types, brute_force_solver, test_graph_generator, non_overlapping_set_tester


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
        g = problem_io.read_problem_from_file_of_name("test_data/test1.json")
        self.assertEquals(g.faulty_set, {"1","3","5"}, "Faulty set read from problem description %s" % (g.faulty_set,))
        self.assertTrue(graph_equal(g.problem_graph.graph, self.problem1_graph), "should get right graph")
        self.assertEquals(g.problem_graph.source, "START", "Source should be START but is %s" % (g.problem_graph.source))
        self.assertEquals(g.problem_graph.sink, "END", "Source should be START but is %s" % (g.problem_graph.sink))

    def test_write_problem_to_file(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(1,3)
        g.add_edge(2,4)
        g.add_edge(3,4)
        start, stop = 1, 4
        graph = base_types.ProblemGraph(g, start, stop)
        faulty_nodes = {2,}
        problem = base_types.Problem(graph, faulty_nodes, "Description of a problem")
        f = StringIO.StringIO()
        problem_io.write_problem_to_file(problem, f)
        self.assertEqual(f.getvalue(), """{"graph": {"sink_node": "4", "edges": {"1": ["2", "3"], "3": ["4"], "2": ["4"], "4": []}, "source_node": "1"}, "version": "0.1", "type": "group testing problem", "description": ["Description of a problem"], "faulty_nodes": ["2"]}""")

    def test_path_tester(self):
        g = problem_io.read_problem_from_file_of_name("test_data/test1.json")
        stats = base_types.TestStatistics()
        path_tester = non_overlapping_set_tester.NonOverlappingSetTester(g.faulty_set, stats)
        p1 = ["2","4","6"]
        p2 = ["1","4","6"]
        p3 = ["2","3","6"]
        [result] = path_tester.test_paths([p1])
        self.assertFalse(result, "For %s path test1 should give negative result" % (p1,))
        [result] = path_tester.test_paths([p2])
        self.assertTrue(result, "For %s path test1 should give positive result" % (p2,))
        [result] = path_tester.test_paths([p3])
        self.assertTrue(result, "For %s path test1 should give positive result" % (p3,))
        self.assertEquals(stats.get_var('positive'), 2, "Should be two positive queries got %d" % (stats.get_var('positive'),))
        self.assertEquals(stats.get_var('negative'), 1, "Should be one negative queries got %d" % (stats.get_var('negative'),))
        self.assertEquals(stats.get_var('all'), 3, "Should be 3 queries in total got %d" % (stats.get_var('all'),))


    def test_brute_force_solver(self):
        g = problem_io.read_problem_from_file_of_name("test_data/test1.json")
        statistics = base_types.TestStatistics()
        tester = non_overlapping_set_tester.NonOverlappingSetTester(g.faulty_set, statistics)
        solver = brute_force_solver.BruteForceGCGTSolver(g, tester)
        faulty_set = solver.solve()
        self.assertEquals(faulty_set, g.faulty_set, "Should find all nodes from faulty set %s, got only %s" %
                          (g.faulty_set, faulty_set))
        self.assertEquals(statistics.get_var('all'), 8, "Should have 8 queries in total got %d" % (statistics.get_var('all'),))
        self.assertEquals(statistics.get_var('positive'), 7, "Should have 7 positive queries in total got %d" % (statistics.get_var('positive'),))
        self.assertEquals(statistics.get_var('negative'), 1, "Should have 1 negative queries in total got %d" % (statistics.get_var('negative'),))

    def test_brute_force_solver2(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(2,4)
        g.add_edge(1,3)
        g.add_edge(3,4)
        g.add_edge(3,5)
        g.add_edge(5,4)

        graph = base_types.ProblemGraph(g, 1, 4)
        problem = base_types.Problem(graph, {5}, None)
        statistics = base_types.TestStatistics()
        tester = non_overlapping_set_tester.NonOverlappingSetTester(problem.faulty_set, statistics)
        solver = brute_force_solver.BruteForceGCGTSolver(problem, tester)
        faulty_set = solver.solve()
        self.assertEqual(faulty_set, {5})

    def test_is_dag_connected(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(2,3)
        g.add_edge(1,3)
        g.add_edge(4,5)
        self.assertFalse(nx.is_weakly_connected(g))

    def test_is_not_consistent_dag_weakly_connected(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(1,3)
        self.assertTrue(nx.is_weakly_connected(g))

    def test_is_not_consistent_dag_marked_not_consistent(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(1,3)
        with self.assertRaises(test_graph_generator.TestGraphException):
            test_graph_generator.get_start_stop_vertex(g)

    def test_is_consistent_dag_marked_consistent(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(1,3)
        g.add_edge(2,4)
        g.add_edge(3,4)
        self.assertEqual(test_graph_generator.get_start_stop_vertex(g), (1,4))

    def test_generate_paths_generates_whole_path(self):
        g = nx.DiGraph()
        g.add_edge(1,2)
        g.add_edge(2,3)
        g.add_edge(3,4)
        all_paths = list(brute_force_solver.generate_paths(g, 1,4))
        self.assertEqual(len(all_paths), 1)
        self.assertEqual([1,2,3,4], list(brute_force_solver.generate_paths(g, 1,4))[0])

if __name__ == "__main__":
    pass
