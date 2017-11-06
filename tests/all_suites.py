# -*- coding: utf-8 -*-
__author__ = 'Stefan Kögl'

import unittest
from tests.viur_relations import update_level_suite

all_suites = unittest.TestSuite([update_level_suite])

runner=unittest.TextTestRunner(verbosity=3)
runner.run(all_suites)
