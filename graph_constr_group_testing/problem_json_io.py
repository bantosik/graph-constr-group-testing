import collections
import json
import networkx as nx

Problem = collections.namedtuple("Problem", ["problem_graph", "faulty_set", "description"])
ProblemGraph = collections.namedtuple("ProblemGraph", ["graph", "source", "sink"])

def read_problem_from_file(file):
    with open(file, "r") as f:
        data = json.load(f)
        
        faulty_set = set(data['faulty_nodes'])
        problem_graph = create_problem_graph(data['graph'])
        if "description" in data:
            description = "".join(data['description'])
        else:
            description = ""
        
        problem = Problem(problem_graph, faulty_set, description)
        
    return problem

def create_problem_graph(data_source):
    graph = nx.DiGraph(data_source['edges'])
    source = data_source['source_node']
    sink = data_source['sink_node']
    problem_graph = ProblemGraph(graph, source, sink)
    return problem_graph