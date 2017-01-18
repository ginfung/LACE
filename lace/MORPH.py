from __future__ import division
import random
import math
import toolkit

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.2"
__email__ = "jchen37@ncsu.edu"


"""
morph is an instance mutator that "shake" the data while maintain the data attributes. GOAL: the MORPHed data
    can be learned by other data-mining techniques as well as the original data.

Version 1.0--Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def simplify_morph(data, alpha, beta):
    """
    same as MOPRH. But require
    1) data is handled, no header, class at last column
    2) data has been normalized
    """
    classes = map(list, zip(*data))[-1]

    if len(set((classes))) == 1:
        return data

    for row_index, row in enumerate(data):  # for each row
        heterogeneous_index = [i for i in range(len(data)) if classes[i] != row[-1]]
        boundary_dist = min([toolkit.euclidean_dist(row, data[heg]) for heg in heterogeneous_index])
        boundary_dist /= math.sqrt(len(data[0])-2)
        for i in range(len(row)):
            data[row_index][i] += boundary_dist * random.uniform(alpha, beta) * random.choice([1, -1])  # shake
    return data


def morph(attribute_names,
          data_matrix,
          independent_attrs,
          objective_attr,
          objective_as_binary=False,
          data_has_normalized=False,
          alpha=0.15,
          beta=0.35):
    """
    morph is a instance mutation which can shake the instance within the class boundary
    :param attribute_names: the names of attributes, should match the data_matrix
    :param data_matrix: original data
    :param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
        considered as independent attributes
    :param objective_attr: marking which attribute is the objective to be considered
    :param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
    :param data_has_normalized: telling whether the data matrix has been normalized.
    :param alpha: morph algorithm parameter
    :param beta: morph algorithm parameter
    :return:
    """

    dataset_t = map(list, zip(*data_matrix))
    dataset = list()
    classes = list()
    for d, a in zip(dataset_t, attribute_names):
        if a in independent_attrs:
            dataset.append(d)
        if a == objective_attr:
            classes = list(d)

    dataset = map(list, zip(*dataset))
    dataset = [map(toolkit.str2num, row) for row in dataset]  # str to numeric
    classes = map(toolkit.str2num, classes)

    if objective_as_binary:
        classes = [1 if i > 0 else 0 for i in classes]
    else:
        classes = toolkit.apply_bin_range(classes)

    is_int = [type(i) is int for i in dataset[0]]  # save. for better representation of the output table

    if data_has_normalized:
        #  adding two instance (all zeros and all ones) so that the normalization and de-normalization process
        #  do not damage the original data
        dataset.append([0]*len(dataset[0]))
        dataset.append([1]*len(dataset[0]))

    '''dataset transposed mode begins...'''
    dataset = map(list, zip(*dataset))  # transpose.
    norm_funcs = []
    denorm_funcs = []

    # normalizing

    for attr_index, attr_elements in enumerate(dataset):  # for each attribute elements
        f1, f2 = toolkit.attr_norm(attr_elements)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
        dataset[attr_index] = map(f1, attr_elements)

    '''dataset mode recover...'''
    dataset = map(list, zip(*dataset))  # transpose again.

    for row_index, row in enumerate(dataset):  # for each row
        heterogeneous_index = [i for i in range(len(classes)) if classes[i] != classes[row_index]]
        boundary_dist = min([toolkit.euclidean_dist(row, dataset[heg]) for heg in heterogeneous_index])
        boundary_dist /= math.sqrt(len(independent_attrs)-1)
        for i in range(len(row)):
            dataset[row_index][i] += boundary_dist*random.uniform(alpha, beta)*random.choice([1, -1])  # shake

    '''dataset transposed mode begins...'''
    dataset = map(list, zip(*dataset))  # transpose.
    for attr_index, attr_elements in enumerate(dataset):  # for each attribute elements
        dataset[attr_index] = map(denorm_funcs[attr_index], attr_elements)  # scale to the original
        for i in range(len(dataset[attr_index])):
            if is_int[attr_index]:
                dataset[attr_index][i] = int(round(dataset[attr_index][i]))  # rounding when needed
            else:
                dataset[attr_index][i] = round(dataset[attr_index][i], 4)
    morphed = map(list, zip(*dataset))  # recover to the original mode and finish.

    '''!!morph done!!'''
    if data_has_normalized:
        morphed = morphed[:-2]

    res = list()
    for x, dm in zip(morphed, data_matrix):
        row = list()
        tmp = 0
        for attri, attr in enumerate(attribute_names):
            if attr in independent_attrs:
                row.append(x[tmp])
                tmp += 1
            elif attr == objective_attr:
                row.append(toolkit.str2num(dm[attri]))
            else:
                row.append(dm[attri])
        res.append(row)

    return res
