# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from tests.viur_api import ViurInterface

__author__ = 'Stefan Kögl'


class ViurTestCase(unittest.TestCase):
	"""BaseClass for viur unittests
	"""

	viur_api = None

	def __init__(self, methodName='runTest'):
		super(ViurTestCase, self).__init__(methodName)

	@classmethod
	def setUpClass(cls):
		cls.viur_api = ViurInterface()
		cls.viur_api.login()

	@classmethod
	def tearDownClass(cls):
		cls.viur_api.logout()
