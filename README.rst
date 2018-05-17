===============================
LACE
===============================


.. image:: https://travis-ci.org/Ginfung/LACE.svg?branch=master
        :target: https://travis-ci.org/Ginfung/LACE

.. image:: https://img.shields.io/pypi/v/LACE.svg
        :target: https://pypi.python.org/pypi/LACE


 Lace-scale Assurance of Confidentiality Environment                                                               
* Free software: MIT license
* Documentation: http://lace.readthedocs.io/en/latest/readme.html
* Algorithm design: `Dr. Fayola Peters <http://www.fayolapeters.com/>`_ @ Univ of Limerick, Ireland
* Package development: `Jianfeng Chen <http://www4.ncsu.edu/~jchen37>`_ @ NC State Univ, United States


What is LACE?
-------------                      
                            
LACE, or Large-scale Assurance Configuration Environment, was firsed introduced by Dr. Peters in ICSE2013. In a short, LACE is a data preprocess algorithm. It can help user to remove the sensitive information and implicit association rules inside the date sets, while keep the utility of the data sets, typically for machine learning or big data mining. In our published articiles, we used the data to train learning models and do the prediction.

There are two versions of LACE at this time. The first version, or *lace1* is constructed by two parts-- CLIFF and MORPH. *CLIFF* is to find the most valuable subset among the dataset. *MORPH* is to "shake" the data so that someone else can not reveal the original data and remove the implicit association rules among the attributes.

The second version of LACE, or lace2, assumes there is a bin which contains the privatized data set from other people or insititutions. And lace2 can allow the user to determine what he or she should add to the bin so that it can improve the diversity of the bin. To pratitize the data, MORPH is also used in lace2.

To explore more details of the lace1 and lace2, please see the two papers listed in **Bibtex**.


How to use?
-----------
LACE can be easily installed by `pip`. Check **Installation** and **Usage**.



Bibtex
-------
::

	@inproceedings{peters2015lace2,
	  title={LACE2: better privacy-preserving data sharing for cross project defect prediction},
	  author={Peters, Fayola and Menzies, Tim and Layman, Lucas},
	  booktitle={Proceedings of the 37th International Conference on Software Engineering-Volume 1},
	  pages={801--811},
	  year={2015},
	  organization={IEEE Press}
	}

::
    
	@article{peters2013balancing,
	  title={Balancing privacy and utility in cross-company defect prediction},
	  author={Peters, Fayola and Menzies, Tim and Gong, Liang and Zhang, Hongyu},
	  journal={IEEE Transactions on Software Engineering},
	  volume={39},
	  number={8},
	  pages={1054--1068},
	  year={2013},
	  publisher={IEEE}
	}
