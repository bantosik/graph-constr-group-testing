import numpy


def make_g_matrix(hmatrix, content_bits_number):
    submatrix_to_transpose = hmatrix[:,0:content_bits_number]
    l = numpy.transpose(submatrix_to_transpose)
    return numpy.concatenate([l, numpy.eye(content_bits_number)], axis=1)


def make_binary_vector(i, data_length):
    result = [int(a) for a in bin(i)[2:]]
    n = len(result)
    for i in xrange(data_length - n):
        result.insert(0,0)
    return numpy.array(result)

def gen_multiply(data, generation_matrix):
    s = numpy.size(generation_matrix, 1)
    k = numpy.size(generation_matrix, 0)
    result = numpy.dot(data, generation_matrix) % 2
    return result

class Code(object):
    def __init__(self, generation_matrix, min_distance):
        self._generation_matrix = generation_matrix
        self._min_distance = min_distance
        self._code_length = numpy.size(self._generation_matrix, 1)
        self._data_length = numpy.size(self._generation_matrix, 0)

    def generate_code_words(self):
        for i in xrange(2**self._data_length):
            yield gen_multiply(make_binary_vector(i, self._data_length), self._generation_matrix)

    def __eq__(self, other):
        return (self._generation_matrix == other._generation_matrix).all() and self._min_distance == other._min_distance


def make_set(code_word):
    result = set([])
    for i, elem in enumerate(numpy.nditer(code_word)):
        if elem:
            result.add(i)
    return result


def code_weight(code_word):
    return numpy.sum(code_word)