========
Usage
========

To use LACE in a project::

    import lace # or
    from lace import cliff, morph, lace1, add_to_bin, lace2_simulator


The CLIFF func::
	
	cliff(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4)
        
:param attribute_names: the attribute names. This should match the data_matrix

:param data_matrix: the data to trim

:param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be
    considered as independent attributes

:param objective_attr: marking which attribute is the objective to be considered

:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False

:param cliff_percentage: set up how many records to be remained. By default, it is 0.4

:return: the survived (valued) records

The MORPH func::

	morph(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, data_has_normalized=False, alpha=0.15, beta=0.35)
    
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
    
:param attribute_names: the names of attributes, should match the data_matrix

:param data_matrix:  original data

:param independent_attrs:  set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be considered as independent attributes

:param objective_attr: marking which attribute is the objective to be considered

:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False

:param cliff_percentage: prune rate

:param alpha: parameter 1 in morph, defining the shaking degree

:param beta: parameter 2 in morph, defining the shaking degree


The data selection and processor in LACE2::

	add_to_bin(attribute_names, try2add_data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, morph_alpha=0.15, morph_beta=0.35, passing_bin=None)

:param attribute_names: the names of attributes, should match the data_matrix

:param try2add_data_matrix: the data anyone is holding

:param independent_attrs: set up the independent attributes in the dataset. Note: 'name', 'id', etc. might not be considered as independent attributes

:param objective_attr: marking which attribute is the objective to be considered

:param objective_as_binary: signal to set up whether treat the objective as a binary attribute. Default: False

:param cliff_percentage: prune rate

:param morph_alpha:  parameter 1 in morph, defining the shaking degree

:param morph_beta: parameter 2 in morph, defining the shaking degree

:param passing_bin: the data get from someone else. Set None if no passing data

:return: the new passing_bin. NOTE: the result must be assigned to another variable. The parameter pointer will NOT be changed

LACE also provides a simple LACE2 application simulator. It automatically distribute all data to different members UNEQUALLY.::
	
	lace2_simulator(attribute_names, data_matrix, independent_attrs, objective_attr, objective_as_binary=False, cliff_percentage=0.4, morph_alpha=0.15, morph_beta=0.35, number_of_holder=5)
    

Here we have a complete simple example to propess the `data 
<https://gist.github.com/Ginfung/f0a9adc43aa28670e7c006d0d9da8906>`_. *This data is from Data.Gov*

::

    import lace
    import csv

    with open('example.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list()
        for line in reader:
            data.append(line)

    attribute_names = header
    data_matrix = data
    independent_attrs = ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3']
    objective_attr = 'mn_earn_wne_p7'

    aftercliff = lace.cliff(attribute_names, data_matrix, independent_attrs, objective_attr, False, 0.4)
    assert len(aftercliff) < 600

    aftermorph = lace.morph(attribute_names, aftercliff, independent_attrs, objective_attr, False, False, 0.15, 0.35)
    assert len(aftermorph)==len(aftercliff) and aftermorph[0] != aftercliff[0]


    lace1res = lace.lace1(attribute_names, data_matrix, independent_attrs, objective_attr, False, 0.4, 0.15,0.35)
    assert len(lace1res) < len(data)*0.5

    bins = [header] + data[:50]
    try2add_data_matrix = data[200:700]
    bins = lace.add_to_bin(attribute_names, try2add_data_matrix, independent_attrs, objective_attr, False, 0.4, 0.15, 0.35, bins)
    assert len(bins) < 550


    lace2res = lace.lace2_simulator(attribute_names, data_matrix, independent_attrs, objective_attr, False, 0.4, 0.15, 0.35, number_of_holder=5)
    assert len(lace2res)<len(lace1res)

