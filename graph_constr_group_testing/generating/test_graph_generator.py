import random
import networkx as nx
from graph_constr_group_testing.core import base_types

class TestGraphException(Exception):
    pass

def generate_dag(n):
    dag = nx.DiGraph()
    for i in range(n):
        for j in range(i):
            if bool(random.randint(0,1)):
                dag.add_edge(j, i)
    return dag


def reachableNodes(g, startNode):
    reachableNodesCount = 0
    for node in nx.dfs_preorder_nodes(g, startNode):
        reachableNodesCount += 1
    return reachableNodesCount

def get_start_stop_vertex(g):
    n = g.number_of_nodes()
    t = nx.topological_sort(g)
    potentialStart = t[0]
    potentialEnd = t[-1]
    reversedGraph = g.reverse(copy=True)

    if reachableNodes(g, potentialStart) == n and reachableNodes(reversedGraph, potentialEnd) == n:
        return potentialStart, potentialEnd
    else:
        raise TestGraphException()

def generate_connected_dag(n):
    g = generate_dag(n)
    while True:
        try:
            start, stop = get_start_stop_vertex(g)
            break
        except TestGraphException:
            g = generate_dag(n)

    return base_types.ProblemGraph(g, start, stop)


def faulty_nodes(problemGraph, d):
    normalNodes = [node for node in problemGraph.graph.nodes_iter() if not node in [problemGraph.source, problemGraph.sink]]
    return set(random.sample(normalNodes, d))



def generate_random_problem_description(n, d):
    """
    :param n: number of internal nodes (not counting start and sink node)
    :param d: number of faulty nodes (it will be some subset of size d of internal nodes)
    """
    #first generate random dag
    problemGraph = generate_connected_dag(n + 2)
    f_nodes = faulty_nodes(problemGraph, d)
    return base_types.GCGTProblem(problem_graph=problemGraph, faulty_set=f_nodes, description=None)