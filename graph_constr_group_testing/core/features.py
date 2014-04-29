def size_of_problem(problem):
    return {'size': problem.problem_graph.graph.number_of_nodes() - 2}

def id(tag, element):
    return {tag: element}