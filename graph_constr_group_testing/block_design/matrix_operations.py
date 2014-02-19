__author__ = 'bartek'
import numpy

class NumpyMatrix(object):
    def __init__(self, array):
        self._m = array
        self._row_size = numpy.size(self._m, 0)

    @classmethod
    def make_matrix(cls, iterable_of_set, elements_num, iterable_length):
        matrix = numpy.zeros(shape=(iterable_length, elements_num))
        for index, sett in enumerate(iterable_of_set):
            for el in sett:
                matrix[index, el] = 1
        return cls(matrix)

    def sum_columns(self, combination):
        return sum(combination, NumpyColumn.make_column_from_iter([0 for i in xrange(self._row_size)]))

    def get_column(self, column_index):
        return NumpyColumn(self._m[:, [column_index]])

    def column_contained(self, column_index, column_containing):
        column = self.get_column(column_index)
        return column.contained_in(column_containing)

    def  get_columns(self):
        col_count = numpy.size(self._m, 1)
        return [self.get_column(i) for i in range(col_count)]

class NumpyColumn(object):
    def __init__(self, array):
        self.v = array

    @classmethod
    def make_column(cls, combination, length):
        v = numpy.zeros([length, 1])
        for el in combination:
            v[el, 0] = 1
        return cls(v)

    @classmethod
    def make_column_from_iter(cls, it):
        v = numpy.array(it)
        size = v.size
        return cls(v.reshape(size, 1))

    def __add__(self, other):
        return NumpyColumn(self.v + other.v)

    def contained_in(self, column_containing):
        return (((1 - self.v) + column_containing.v) > 0).all()


