import json
import networkx as nx
from graph_constr_group_testing import base_types

SOURCE_NODE_TAG = 'source_node'
SINK_NODE_TAG = 'sink_node'
EDGES_TAG = 'edges'

DESCRIPTION_TAG = 'description'
GRAPH_TAG = 'graph'
NODES_TAG = 'faulty_nodes'


def read_problem_from_file(f):
    data = json.load(f)
    faulty_set = set(data[NODES_TAG])
    problem_graph = _create_problem_graph(data[GRAPH_TAG])
    description = "".join(data.get(DESCRIPTION_TAG, ''))
    problem = base_types.Problem(problem_graph, faulty_set, description)
    return problem


def read_problem_from_file_of_name(filename):
    with open(filename, "r") as f:
        return read_problem_from_file(f)


def _serialize_graph_to_dict(problem_graph):
    g = problem_graph.graph
    source = str(problem_graph.source)
    sink = str(problem_graph.sink)
    edges = {str(k): [str(key) for key in v.keys()] for k,v in g.adj.iteritems()}
    graph_repr = {EDGES_TAG: edges, SOURCE_NODE_TAG: source, SINK_NODE_TAG: sink}
    return graph_repr


def write_problem_to_file(problem, file):
    faulty_set = list(str(node) for node in problem.faulty_set)
    graph = _serialize_graph_to_dict(problem.problem_graph)
    repr = {GRAPH_TAG: graph, NODES_TAG: faulty_set}
    if problem.description is not None:
        repr[DESCRIPTION_TAG] = [problem.description]
    json.dump(repr, file)


def write_problem_to_file_of_name(problem, filename):
    with open(filename, "wc") as f:
        return write_problem_to_file(problem, f)

def _create_problem_graph(data_source):
    graph = nx.DiGraph(data_source[EDGES_TAG])
    source = data_source[SOURCE_NODE_TAG]
    sink = data_source[SINK_NODE_TAG]
    problem_graph = base_types.ProblemGraph(graph, source, sink)
    return problem_graph