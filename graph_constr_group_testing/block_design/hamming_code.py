import numpy
from graph_constr_group_testing.block_design import linear_codes

__author__ = 'bartek'

def count_positions(n):
    i = 0
    t = n
    while t > 0:
        t = t >> 1
        i += 1
    return i

def count_ones(n):
    i = 0
    t = n
    while t > 0:
        if t & 1:
            i += 1
        t = t >> 1
    return i

def should_go_first(i):
    if count_ones(i) == 1:
        return False
    else:
        return True


def fill_column(hmatrix, k, i):
    value = i
    bit = 0
    while value > 0:
        if value & 1:
            hmatrix[bit, k] = 1
        value = value >> 1
        bit += 1

def generation_matrix(num_of_encoding_bits):
    #assert num of bits in the form 2^n - 1
    assert ~ ((num_of_encoding_bits) & (num_of_encoding_bits + 1))
    parity_bits_number = count_positions(num_of_encoding_bits)
    content_bits_number = num_of_encoding_bits - parity_bits_number
    hmatrix = numpy.zeros((num_of_encoding_bits - content_bits_number, num_of_encoding_bits))
    last_column = num_of_encoding_bits - 1
    first_column = 0
    for i in xrange(1, num_of_encoding_bits + 1):
        if should_go_first(i):
            k = first_column
            first_column += 1
        else:
            k = last_column
            last_column -= 1
        fill_column(hmatrix, k, i)
    return linear_codes.make_g_matrix(hmatrix, content_bits_number)

def get_code(num_of_encoding_bits):
    return linear_codes.Code(generation_matrix(num_of_encoding_bits), 3)
