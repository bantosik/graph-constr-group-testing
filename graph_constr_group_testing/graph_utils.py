import random

__author__ = 'Bartek'

def generate_paths(graph, start_point, end_point):
    if start_point == end_point:
        yield [end_point]
    else:
        for begin, end in graph.out_edges(start_point):
            for p in generate_paths(graph, end, end_point):
                yield [begin] + p

def random_path_generator(graph, start_point, end_point, seed):
    random.seed(seed)
    while True:
        current_node = start_point
        path = [current_node]
        while current_node != end_point:
            current_node = random.sample(graph.out_edges(current_node), 1)[0][1]
            path.append(current_node)
        yield path