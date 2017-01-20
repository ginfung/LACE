from __future__ import division
import CLIFF
import MORPH
import LeaF
import toolkit
import random
import copy

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "3.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE2 means cliff + LeaF + morph
This file is the control flow of LACE2.
Given the dataset, return the result of LACE2.
"""


def add_to_bin(attribute_names,
               try2add_data_matrix,
               independent_attrs,
               objective_attr,
               objective_as_binary=False,
               cliff_percentage=0.4,
               morph_alpha=0.15,
               morph_beta=0.35,
               passing_bin=None
               ):
    """
    LACE2 data paring engine
    :param attribute_names: the names of attributes, should match the data_matrix
    :param try2add_data_matrix: the data anyone is holding
    :param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
        considered as independent attributes
    :param objective_attr: marking which attribute is the objective to be considered
    :param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
    :param cliff_percentage: prune rate
    :param morph_alpha:  parameter 1 in morph, defining the shaking degree
    :param morph_beta: parameter 2 in morph, defining the shaking degree
    :param passing_bin: the data get from someone else. Set None if no passing data
    :return: the new passing_bin.
        NOTE: the result must be assigned to another variable. The parameter pointer will NOT be changed
    """
    if passing_bin is not None:
        assert passing_bin[0] == attribute_names, "new added table should share the same table with existed BIN data"
    else:
        passing_bin = [attribute_names]

    my = list()
    others = list()

    # prepare for the core independent+dependent dataset
    for attr in independent_attrs:
        col = zip(*try2add_data_matrix)[attribute_names.index(attr)]
        col = map(toolkit.str2num, col)
        my.append(col)

        if len(passing_bin)>2:
            other_col = zip(*passing_bin[1:])[attribute_names.index(attr)]
            other_col = map(toolkit.str2num, other_col)
            others.append(other_col)

    classes = zip(*try2add_data_matrix)[attribute_names.index(objective_attr)]
    obj = classes[:]
    other_classes = zip(*passing_bin[1:])[attribute_names.index(objective_attr)] if len(passing_bin) > 2 else []
    classes = map(toolkit.str2num, classes)
    other_classes = map(toolkit.str2num, other_classes)

    if objective_as_binary:
        classes = [1 if i > 0 else 0 for i in classes]
        other_classes = [1 if i > 0 else 0 for i in other_classes]
    else:
        classes = toolkit.apply_bin_range(classes)
        other_classes = toolkit.apply_bin_range(other_classes)

    my.append(classes)
    others.append(other_classes)
    my = map(list, zip(*my))

    protected_line = copy.deepcopy(my[0])  # saving the data formats!
    others = map(list, zip(*others))

    # normalization process
    norm_funcs, denorm_funcs = list(), list()
    for col in map(list, zip(*my+others)):
        f1, f2 = toolkit.attr_norm(col)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
    cache = list()

    # normalizing my
    uni_my = list()
    my = map(list, zip(*my))
    for funi, col in enumerate(my[:-1]):
        uni_my.append(map(norm_funcs[funi], col))
    uni_my.append(my[-1])
    my = map(list, zip(*uni_my))

    if len(passing_bin) < 2:
        cache = CLIFF.cliff_core(my, cliff_percentage, objective_as_binary, handled_obj=True)
    else:
        # normalizing others
        uni_others = list()
        others = map(list, zip(*others))
        for funi, col in enumerate(others[:-1]):
            uni_others.append(map(norm_funcs[funi], col))
        uni_others.append(others[-1])
        others = map(list, zip(*uni_others))

        to_submits = CLIFF.cliff_core(my, cliff_percentage, objective_as_binary, handled_obj=True)
        bins = others

        fetch_num = min(len(my) + len(others), 100)
        sampled = random.sample(my + others, fetch_num)
        sampled_obj = zip(*sampled)[-1]
        sampled = toolkit.normalize_cols_for_table([row[:-1] for row in sampled])
        sampled = [i + [j] for i, j in zip(sampled, sampled_obj)]

        inter_class_dist = LeaF.find_distinct_distance(sampled)
        for test in to_submits:
            if LeaF.whether_add_to_private_cache(my[test], bins, inter_class_dist):
                cache.append(test)
                # bins.append(my[test])

    if len(cache) == 0:
        return passing_bin

    cache_data = [my[i] for i in cache]
    cache_obj = [obj[i] for i in cache]
    cache_data = MORPH.simplify_morph(cache_data+others, morph_alpha, morph_beta)[:len(cache_data)]

    for at, i in enumerate(cache):
        h = try2add_data_matrix[i]
        new = cache_data[at]
        new2 = [func(d) for func, d in zip(denorm_funcs, new)]
        new = new2
        c = cache_obj[at]

        row = list()
        new_c = 0
        for h_c, attr in enumerate(attribute_names):
            if attr == objective_attr:
                row.append(c)
                continue
            if attr in independent_attrs:
                row.append(new[new_c])
                new_c += 1
                continue
            else:
                row.append(h[h_c])
        row = map(str, row)
        passing_bin.append(row)
    return passing_bin


def lace2_simulator(attribute_names,
                    data_matrix,
                    independent_attrs,
                    objective_attr,
                    objective_as_binary=False,
                    cliff_percentage=0.4,
                    morph_alpha=0.15,
                    morph_beta=0.35,
                    number_of_holder=5
                    ):
    """
    This is a simulator. Distribute to the data to different members UNEQUALLY.
    :return: list of list. each of list represent a data set holder by one person
    """
    data = copy.deepcopy(data_matrix)  # protect the original parameters
    n = len(data)

    part_size = [random.uniform(0, 1) for _ in xrange(number_of_holder)]
    s = sum(part_size)
    part_size = sorted(map(lambda x: int(n/s*x), part_size))
    # correction
    corr = n - sum(part_size)
    if corr > 0:
        for i in range(0, corr):
            part_size[i] += 1
    if corr < 0:
        for i in range(number_of_holder - corr, number_of_holder):
            part_size[i] -= 1

    random.shuffle(data)

    holdings = []
    cursor = 0
    for i in part_size:
        holdings.append(data[cursor: cursor+i])
        cursor += i

    random.shuffle(holdings)
    passing_bin = None
    for holding in holdings:
        passing_bin = add_to_bin(attribute_names,
                                 holding,
                                 independent_attrs,
                                 objective_attr,
                                 objective_as_binary,
                                 cliff_percentage,
                                 morph_alpha,
                                 morph_beta,
                                 passing_bin)
    return passing_bin
