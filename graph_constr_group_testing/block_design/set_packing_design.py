r"""Set packing design is method to construct d-disjunct matrices introduced in
It is deterministic construction method. Authors introduced concept of :math:`t`-:math:`(v,k,{\lambda})` *packing* *design*
It is a family :math:`F` of of :math:`k` subsets of a :math:`V` a :math:`v`-element set such that any :math:`t`-size subset of :math:`V` is contained
is contained in at most :math:`{\lambda}` of :math:`F`"""
import itertools
import numpy


def make_vector(combination, length):
    v = numpy.zeros([length, 1])
    for el in combination:
        v[el, 0] = 1
    return v

def sum_columns(m, combination):
    length = numpy.size(m, 1)
    v = make_vector(combination, length)
    return numpy.dot(m, v)

def get_column(matrix, column_index):
    return matrix[:, [column_index]]

def contained_in(column, column_containing):
    return ((1 - column) + column_containing > 0).all()

def column_contained(matrix, column_index, column_containing):
    column = get_column(matrix, column_index)
    return contained_in(column, column_containing)

def get_columns(m):
    return range(numpy.size(m, 1))

def is_d_disjunct(m, d):
    columns = get_columns(m)
    for combination in itertools.combinations(columns, d):
        sum = sum_columns(m, combination)
        for k in columns:
            if k not in combination:
                if column_contained(m, k, sum):
                    return False

    else:
        return True



def _is_packing_design(set_family, all_items):
    pass


def make_matrix(iterable_of_set, elements_num, iterable_length):
    matrix = numpy.zeros(shape=(iterable_length, elements_num))
    for index, sett in enumerate(iterable_of_set):
        for el in sett:
            matrix[index, el] = 1
    return matrix

