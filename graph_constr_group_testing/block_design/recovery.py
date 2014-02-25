__author__ = 'bartek'
def recover_from_disjunct(matrix, result_column, d):
    cols = matrix.get_columns()
    result = []
    for i, column in enumerate(cols):
        if column.contained_in(result_column):
            result.append(i)
    return result








