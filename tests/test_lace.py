#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lace
----------------------------------

Tests for `lace` module.
"""

import unittest
import csv
import lace

class TestLace(unittest.TestCase):
    def setUp(self):
        with open('tests/sample_data/school.csv', 'r') as f:
            reader = csv.reader(f)
            self.header = next(reader)
            self.data = list()
            for line in reader:
                self.data.append(line)

    def test_something(self):
        # testing cliff
        aftercliff = lace.cliff(self.header,
                   self.data,
                   ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                   'mn_earn_wne_p7',
                   False,
                   0.3)
        assert len(aftercliff) < 600, "It seems the CLIFF did not prune the data!"

        # testing morph
        aftermorph = lace.morph(self.header,
                         aftercliff,
                         ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                         'mn_earn_wne_p7',
                         False,
                         False,
                         0.15,
                         0.35)
        assert len(aftermorph)==len(aftercliff) and aftermorph[0] != aftercliff[0]

        # testing lace1
        lace1res = lace.lace1(self.header,
                              self.data,
                              ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                              'mn_earn_wne_p7',
                              False,
                              0.3,
                              0.15,
                              0.3)
        assert len(lace1res) < len(self.data)*0.5 and lace1res not in self.data
        
        # testing lace2 core
        bins = [self.header]+self.data[:50]
        lace.add_to_bin(self.header,
                        self.data[200:700],
                        ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                        'mn_earn_wne_p7',
                        False,
                        0.4,
                        0.15,
                        0.35,
                        bins
                        )
        assert len(bins) < 550, "LACE2 core engergy not working"
    
        # tesing lace2 simulator
        lace2res = lace.lace2_simulator(self.header,
                             self.data,
                             ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                             'mn_earn_wne_p7',
                             False,
                             0.4,
                             0.15,
                             0.35,
                             5)
        assert len(lace2res)<len(lace1res), "LACE2 did not prune more than lace1 engine. check the code again."
    
    def tearDown(self):
        pass
