from graph_constr_group_testing.core import base_types

class NonOverlappingSetTester(base_types.SetTester):
    """
    Simulator of testing system.

    Objects of this class will be used for testing paths by solver objects. State
    of the testing system is passed in the constructor, :func:`test_paths` function is used by solver.
    """
    def __init__(self, faulty_set, stats):
        """
        :param faulty_set: set of faulty elements. Existence of it will be tested in NonOverlappingPathTester.test_paths
        :type faulty_set: set
        :param stats: object to which various aspects of computation will be reported
        :type stats: base_types.TestStatistics
        """
        self.faulty_set = faulty_set
        self.stats = stats

    def test_paths(self, paths):
        results = []
        for path in paths:
            result = any((x in self.faulty_set) for x in path)
            results.append(result)
            if result:
                self.stats.inc_var('positive')
            else:
                self.stats.inc_var('negative')
            self.stats.inc_var('all')
        self.stats.inc_var('tests')
        return results