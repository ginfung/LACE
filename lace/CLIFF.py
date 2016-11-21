#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from __future__ import division
import copy
import logging
import random
import toolkit

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"

"""
cliff algorithm
Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def power(L, C, Erange):
    """
    :param L: a list of values for one attribute in the data set
    :param C: the class corresponded to L list
    :param Erange: a st of sub-range for a given attribute. specifically, it's the boundary returned from binrange()
    :return: the power of each item in this attribute
    """
    assert len(L) == len(C), "The L and C must be corresponded to each other"
    E = copy.deepcopy(Erange)
    E[0] -= 1

    power_table = dict()
    for c in set(C):  # for each type of class
        first = [index for index, eachc in enumerate(C) if eachc == c]
        rest = [index for index, eachc in enumerate(C) if eachc != c]
        p_first = len(first) / len(L)
        p_rest = len(rest) / len(L)

        powerc = []
        for u, v in zip(E[0:-1], E[1:]):  # checking the range (u,v]
            like_first = sum([1 for i in first if u < L[i] <= v]) / len(first) * p_first
            like_rest = sum([1 for i in rest if u < L[i] <= v]) / len(rest) * p_rest
            try:
                powerc.append((like_first ** 2 / (like_first + like_rest)))
            except ZeroDivisionError:
                powerc.append(0)
        power_table[c] = powerc

    # filling the result by power_table
    power = []
    for l, c in zip(L, C):
        for e_cursor in range(len(E)):
            if E[e_cursor] >= l: break
        power.append(round(power_table[c][e_cursor - 1], 2))

    return power


def cliff_core(data, percentage, obj_as_binary, handled_obj=False):
    """
    data has no header, only containing the record attributes
    :return the cliffed data INDICES(part of the input data)
    """

    if len(data) < 50:
        logging.debug("no enough data to cliff. return the whole dataset")
        return range(len(data))

    # percentage /= 100 if percentage > 1 else 1

    classes = map(toolkit.str2num, zip(*data)[-1])

    if not handled_obj:
        if obj_as_binary:
            classes = [1 if i > 0 else 0 for i in classes]
        else:
            classes = toolkit.apply_bin_range(classes)

    data_power = list()  # will be 2D list (list of list)

    for col in zip(*data):
        col = map(toolkit.str2num, col)
        E = toolkit.binrange(col)
        data_power.append(power(col, classes, E))

    data_power = map(list, zip(*data_power))  # transposing the data power
    row_sum = [sum(row) for row in data_power]

    index = range(len(data))
    zips = zip(data, classes, row_sum, index)

    output = list()
    for cls in set(classes):
        matched = filter(lambda z: z[1] == cls, zips)
        random.shuffle(matched)
        matched = sorted(matched, key=lambda z: z[2], reverse=True)

        if len(matched) < 5:
            output.extend([m[3] for m in matched])  # all saved
            continue

        for i in range(int(len(matched) * percentage)):
            output.append(matched[i][3])
    return sorted(output)


def cliff(attribute_names,
          data_matrix,
          independent_attrs,
          objective_attr,
          objective_as_binary=False,
          cliff_percentage=0.4):
    """
    Core function for cliff algorithm
    prune the data set according to the power
    attributes are discrete

    :param attribute_names: The attribute names. This should match the data_matrix
    :param data_matrix: the data to trim
    :param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
        considered as independent attributes
    :param objective_attr: marking which attribute is the objective to be considered
    :param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
    :param cliff_percentage: set up how many records to be remained. By default, it is 0.4
    :return: The survived (valued) records
    """
    ori_attrs, alldata = attribute_names, data_matrix  # load the database

    alldata_t = map(list, zip(*alldata))
    valued_data_t = list()
    for attr, col in zip(ori_attrs, alldata_t):
        if attr in independent_attrs:
            valued_data_t.append(col)
    valued_data_t.append(alldata_t[attribute_names.index(objective_attr)])  # cant miss the classification

    alldata = map(list, zip(*valued_data_t))
    alldata = map(lambda row: map(toolkit.str2num, row), alldata)  # numbering the 2d table

    after_cliff = cliff_core(alldata, cliff_percentage, objective_as_binary)

    res = [data_matrix[i] for i in after_cliff]

    return res
