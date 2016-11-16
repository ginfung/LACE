#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lace
----------------------------------

Tests for `lace` module.
"""

import unittest

import lace


class TestLace(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert(lace.__version__)

    def tearDown(self):
        pass
