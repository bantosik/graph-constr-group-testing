r"""Set packing design is method to construct d-disjunct matrices introduced in
It is deterministic construction method. Authors introduced concept of :math:`t`-:math:`(v,k,{\lambda})` *packing* *design*
It is a family :math:`F` of of :math:`k` subsets of a :math:`V` a :math:`v`-element set such that any :math:`t`-size subset of :math:`V` is contained
is contained in at most :math:`{\lambda}` of :math:`F`. This code assumes that :math:`{\lambda} = 1`"""
import itertools


def is_d_disjunct(m, d):
    columns = m.get_columns()
    for col_combination in itertools.combinations(columns, d):
        sum = m.sum_columns(col_combination)
        for column in columns:
            if column not in col_combination:
                if column.contained_in(sum):
                    return False

        else:
            return True


def is_packing_design(sets, t, v):
    return all(not any(comb in sett for sett in sets) for comb in itertools.combinations(range(v), t))

