========
Usage
========

To use LACE in a project::

    import lace


The CLIFF func::
	
	def CLIFF(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4):
    """
    Core function for CLIFF algorithm
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

The MORPH func::

	function morph(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, data_has_normalized=False, alpha=0.15, beta=0.35):
    
    Parameters:
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

The most convenient way to use LACE1 is::

	function lace1(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, alpha=0.15, beta=0.35):
    
    Parameters:
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