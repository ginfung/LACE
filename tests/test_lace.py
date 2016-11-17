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
        aftercliff = lace.CLIFF(self.header,
                   self.data,
                   ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                   'mn_earn_wne_p7',
                   False,
                   0.3)
        assert(len(aftercliff) < 500, "It seems the CLIFF did not prune the data!")

        aftermorph = lace.MORPH(self.header,
                         aftercliff,
                         ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                         'mn_earn_wne_p7',
                         False,
                         False,
                         0.15,
                         0.35)
        assert(len(aftermorph)==len(aftercliff) and aftermorph[0] != aftercliff[0])
    
        lace1res = lace.lace1(self.header,
                              self.data,
                              ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'],
                              'mn_earn_wne_p7',
                              False,
                              0.3,
                              0.15,
                              0.3)
        assert(len(lace1res) < len(self.data)*0.5 and lace1res not in self.data)
    
    def tearDown(self):
        pass
