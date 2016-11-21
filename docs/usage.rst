========
Usage
========

To use LACE in a project::

    import lace


The CLIFF func::
	
	CLIFF(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4)
        
Parameters:
:param attribute_names: The attribute names. This should match the data_matrix
:param data_matrix: the data to trim
:param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
    considered as independent attributes
:param objective_attr: marking which attribute is the objective to be considered
:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
:param cliff_percentage: set up how many records to be remained. By default, it is 0.4
:return: The survived (valued) records

The MORPH func::

	morph(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, data_has_normalized=False, alpha=0.15, beta=0.35)
    
Parameters:
:param attribute_names: the names of attributes, should match the data_matrix
:param data_matrix: original data
:param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be considered as independent attributes
:param objective_attr: marking which attribute is the objective to be considered
:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
:param data_has_normalized: telling whether the data matrix has been normalized.
:param alpha: morph algorithm parameter
:param beta: morph algorithm parameter
:return: handled records

The most convenient way to use LACE1 is::

	lace1(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, alpha=0.15, beta=0.35)
    
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

The data selection and processor in LACE2::

	add_to_bin(attribute_names, try2add_data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, morph_alpha=0.15, morph_beta=0.35, passing_bin=None)

Parameters:
:param attribute_names: the names of attributes, should match the data_matrix
:param try2add_data_matrix: the data anyone is holding
:param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be considered as independent attributes
:param objective_attr: marking which attribute is the objective to be considered
:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False
:param cliff_percentage: prune rate
:param morph_alpha:  parameter 1 in morph, defining the shaking degree
:param morph_beta: parameter 2 in morph, defining the shaking degree
:param passing_bin: the data get from someone else. Set None if no passing data
:return: the new passing_bin.
    NOTE: the result must be assigned to another variable. The parameter pointer will NOT be changed

LACE also provides a simple LACE2 application simulator. It automatically distribute all data to different members UNEQUALLY.::
	lace2_simulator(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, morph_alpha=0.15, morph_beta=0.35, number_of_holder=5)
    



