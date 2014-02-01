import json
import networkx as nx
from graph_constr_group_testing import base_types


def read_problem_from_file(f):
    data = json.load(f)
    faulty_set = set(data['faulty_nodes'])
    problem_graph = _create_problem_graph(data['graph'])
    description = "".join(data.get('description', ''))
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
    graph_repr = {'edges': edges, 'source_node': source, 'sink_node': sink}
    return graph_repr


def write_problem_to_file(problem, file):
    description = [problem.description]
    faulty_set = list(str(node) for node in problem.faulty_set)
    graph = _serialize_graph_to_dict(problem.problem_graph)
    repr = {'graph': graph, 'faulty_nodes': faulty_set, 'description': description}
    json.dump(repr, file)


def write_problem_to_file_of_name(problem, filename):
    with open(filename, "wc") as f:
        return write_problem_to_file(problem, f)

def _create_problem_graph(data_source):
    graph = nx.DiGraph(data_source['edges'])
    source = data_source['source_node']
    sink = data_source['sink_node']
    problem_graph = base_types.ProblemGraph(graph, source, sink)
    return problem_graph