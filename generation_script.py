import os
import sys
from graph_constr_group_testing.generating import test_graph_generator
import argparse
from graph_constr_group_testing.io import problem_json_io

parser = argparse.ArgumentParser()
parser.add_argument('--min', dest='min', type=int)
parser.add_argument('--max', dest='max', type=int)
parser.add_argument('-i', dest='instances', type=int)
parser.add_argument('-f', dest='faults', type=int)
parser.add_argument('--dir', dest='dirname', type=str)
args = parser.parse_args()

problem_count = args.instances
faults = args.faults
dirname = args.dirname


def ensure_dir(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def main(min, max, problem_count, faults, dirname):
    sizes_of_problem = xrange(min, max)
    all_of = len(sizes_of_problem)*problem_count

    counter = 0
    for size_of_problem in sizes_of_problem:
        for c in xrange(problem_count):
            sys.stdout.write("\r%.2f%%" % (100*float(counter)/all_of))    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
            counter += 1
            filename = "problem_{size}_{faults}_{idp}.json".format(size=size_of_problem, idp=c, faults=faults)
            filename = os.path.join(dirname, filename)
            ensure_dir(filename)
            problem_description = test_graph_generator.generate_random_problem_description(size_of_problem, faults)
            problem_json_io.write_problem_to_file_of_name(problem_description, filename)
    return 0

if __name__ == "__main__":
    sys.exit(main(args.min, args.max, problem_count, faults, dirname))