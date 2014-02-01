__author__ = 'bartek'

import matplotlib.pyplot as plt
import networkx as nx

from graph_constr_group_testing import test_graph_generator


g = test_graph_generator.generate_dag(15)
nx.draw_graphviz(g, prog='dot')
plt.show()

