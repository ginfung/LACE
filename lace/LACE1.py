from CLIFF import *
from MORPH import *

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE1 means cliff + morph
This file is the control flow of LACE1.
Given the dataset, return the result of LACE1.
"""


def lace1(attribute_names,
          data_matrix,
          independent_attrs,
          objective_attr,
          objective_as_binary=False,
          cliff_percentage=0.4,
          alpha=0.15,
          beta=0.35):
    """
    :param attribute_names: the names of attributes, should match the data_matrix
    :param data_matrix:  original data
    :param independent_attrs:  set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
        considered as independent attributes
    :param objective_attr: marking which attribute is the objective to be considered
    :param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
    :param cliff_percentage: prune rate
    :param alpha: parameter 1 in morph, defining the shaking degree
    :param beta: parameter 2 in morph, defining the shaking degree
    :return:
    """
    after_cliff = cliff(attribute_names, data_matrix, independent_attrs,
                        objective_attr, objective_as_binary, cliff_percentage)
    res = morph(attribute_names, after_cliff, independent_attrs,
                objective_attr, objective_as_binary, False, alpha, beta)
    return res
