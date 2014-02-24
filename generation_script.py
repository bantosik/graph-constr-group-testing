import sys
from graph_constr_group_testing import problem_json_io
from graph_constr_group_testing.generating import test_graph_generator

sizes_of_problem = xrange(4, 20)
problem_count = 30
faults = 1
dirname="test_data/experiment1/"

all_of = len(sizes_of_problem)*problem_count

counter = 0
for size_of_problem in sizes_of_problem:
    for c in xrange(problem_count):
        sys.stdout.write("\r%.2f%%" % (float(counter)/all_of))    # or print >> sys.stdout, "\r%d%%" %i,
        sys.stdout.flush()
        counter += 1
        filename = "{dir}problem_{size}_{faults}_{idp}.json".format(dir=dirname, size=size_of_problem, idp=c, faults=faults)
        problem_description = test_graph_generator.generate_random_problem_description(size_of_problem, faults)
        problem_json_io.write_problem_to_file_of_name(problem_description, filename)
