import collections
import csv
from graph_constr_group_testing.core import base_types

def averageQueriesForSize(results):
    result = []
    count = collections.defaultdict(int)
    sumallqueries = collections.defaultdict(int)
    for solver, problem, statistics in results:
        n = base_types.size_of_problem(problem)
        count[n] += 1
        sumallqueries[n] += statistics.get_var('all')

    for k, v in sumallqueries.iteritems():
        result.append((k, float(v)/count[k]))
    return zip(*sorted(result, key=lambda x: x[0]))

class CsvStats(base_types.ExperimentStatistics):
    def __init__(self, renderers, csvFileName):
        super(CsvStats, self).__init__(renderers)
        self._fileName = csvFileName

    def process(self):
        with open(self._fileName, 'wc') as csvFile:
            writer = csv.DictWriter(csvFile, list(self.headers))
            writer.writeheader()
            writer.writerows(self.results)
