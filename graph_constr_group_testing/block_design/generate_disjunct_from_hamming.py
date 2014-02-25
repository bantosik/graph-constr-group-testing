import math
from graph_constr_group_testing.block_design import hamming_code, linear_codes, matrix_operations

__author__ = 'bartek'


def get_next_power_of_two(x):
    return (1 << (x.bit_length())) - 1

#TODO: if there will be more code for generating d-disjunct matrices from error correcting codes make this polymorphic method of linear_codes.Code class
def estitmate_code_length(universe_size):
    return get_next_power_of_two(int(math.ceil(math.sqrt(6*(universe_size)) + 1)))


def generate_d_disjunct(universe_size):
    k = estitmate_code_length(universe_size)
    code = hamming_code.get_code(k)
    generator = code.generate_code_words()
    code_words_set = []
    try:
        while len(code_words_set) < universe_size:
            code_word = generator.next()
            if linear_codes.code_weight(code_word) == 3:
                code_words_set.append(linear_codes.make_set(code_word))
    except StopIteration:
        raise
    return matrix_operations.NumpyMatrix.make_matrix_from_columns(code_words_set)
