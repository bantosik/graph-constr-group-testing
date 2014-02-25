__author__ = 'bartek'
import numpy


class NumpyRow(object):
    def __init__(self, array):
        self.v = array

    def __iter__(self):
        for i, el in enumerate(numpy.nditer(self.v)):
            if el:
                yield i




class NumpyMatrix(object):
    def __init__(self, array):
        self._m = array
        self._row_size = numpy.size(self._m, 0)
        self._col_size = numpy.size(self._m, 1)

    @classmethod
    def _make_matrix(cls, list_of_set):
        maxx = max(max(sett) for sett in list_of_set)
        iterable_length = len(list_of_set)
        matrix = numpy.zeros(shape=(iterable_length, maxx + 1))
        for index, sett in enumerate(list_of_set):
            for el in sett:
                matrix[index, el] = 1
        return matrix

    @classmethod
    def make_matrix_from_blocks(cls, list_of_set):
        matrix = cls._make_matrix(list_of_set)
        return cls(matrix)

    @classmethod
    def make_matrix_from_columns(cls, list_of_columns):
        matrix = cls._make_matrix(list_of_columns)
        return cls(numpy.transpose(matrix))

    def sum_columns(self, combination):
        return sum(combination, NumpyColumn.make_column_from_iter([0 for i in xrange(self._row_size)]))

    def get_column(self, column_index):
        return NumpyColumn(self._m[:, [column_index]])

    def _get_row(self, row_index):
        return NumpyRow(self._m[[row_index], :])

    def column_contained(self, column_index, column_containing):
        column = self.get_column(column_index)
        return column.contained_in(column_containing)

    def  get_columns(self):
        col_count = numpy.size(self._m, 1)
        return [self.get_column(i) for i in range(col_count)]

    def get_blocks(self):
        row_count = numpy.size(self._m, 0)
        return (self._get_row(i) for i in range(row_count))

    def transpose(self):
        return NumpyMatrix(numpy.transpose(self._m))

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



