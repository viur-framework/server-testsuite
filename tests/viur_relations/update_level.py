# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import time
import unittest
from datetime import datetime

from tests.viur_testcase import ViurTestCase

__author__ = 'Stefan Kögl'


class UpdateLevelTest(ViurTestCase):
	"""We are testing if all updateLevels on relationsBones behave as expected

	updatelevel_0 userBone firstname should change in report refKeys and viur_relations each time it is changed
	updatelevel_1 userBone should only change in report and viur_Relations on updateSearchIndex calls
	updatelevel_2 userBone should only get set once on add or when test destination changed in report itself,
	on each consecutive modifications of dest user it may not change.

	userlevel_3,4,5 extends the tests for multiple=True on the bones.

	We will check the firstname refkey as also the changedate on report entries
	"""

	def __init__(self, methodName='runTest'):
		super(UpdateLevelTest, self).__init__(methodName)

	@classmethod
	def setUpClass(cls):
		"""We're using that method because we are going to test interoperatibility of some add/edit/rebuildSearch commands

		:return:
		"""
		super(UpdateLevelTest, cls).setUpClass()

		# users for single relations
		cls.testUser0 = {
			u"key": None,
			u"name": u"user0@testcase.de",
			u"password": u"aaaBBBCCC12345",
			u"nick": u"user0",
			u"firstname": u"user0_first 1",
			u"lastname": u"user0_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		cls.testUser1 = {
			u"name": u"user1@testcase.de",
			u"password": u"aaaBBBCCC12345",
			u"nick": u"user1",
			u"firstname": u"user1_first 1",
			u"lastname": u"user1_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}
		cls.testUser2 = {
			u"name": u"user2@testcase.de",
			u"password": u"aaaBBBCCC12345",
			u"nick": u"user2",
			u"firstname": u"user2_first 1",
			u"lastname": u"user2_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		# users for multiple relations
		cls.testUser3 = {
			u"name": u"user3@testcase.de",
			u"password": u"aaaBBBCCC13345",
			u"nick": u"user3",
			u"firstname": u"user3_first 1",
			u"lastname": u"user3_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		cls.testUser4 = {
			u"name": u"user4@testcase.de",
			u"password": u"aaaBBBCCC14345",
			u"nick": u"user4",
			u"firstname": u"user4_first 1",
			u"lastname": u"user4_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		cls.testUser5 = {
			u"name": u"user5@testcase.de",
			u"password": u"aaaBBBCCC15345",
			u"nick": u"user5",
			u"firstname": u"user5_first 1",
			u"lastname": u"user5_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		# never change that user
		cls.testUser6 = {
			u"name": u"user6@testcase.de",
			u"password": u"aaaBBBCCC15345",
			u"nick": u"user6",
			u"firstname": u"user6_first 1",
			u"lastname": u"user6_last 1",
			u"status": 10,
			u"skey": cls.viur_api.get_skey()
		}

		cls.testReport = {
			u"key": None,
			u"updatelevel_0.key": None,
			u"updatelevel_1.key": None,
			u"updatelevel_2.key": None,
			u"updatelevel_3_multi.0.key": None,
			u"updatelevel_3_multi.1.key": None,
			u"updatelevel_4_multi.0.key": None,
			u"updatelevel_4_multi.1.key": None,
			u"updatelevel_5_multi.0.key": None,
			u"updatelevel_5_multi.1.key": None,
			u"skey": cls.viur_api.get_skey()
		}

		# initial clear test kinds?
		cls.viur_api.get("report/cleanup")
		time.sleep(6)
		status = cls.viur_api.get("report/checkStatusJson")
		assert status == {"relationList": [], "report": None, "userList": []}

		# adding single users
		response = cls.viur_api.add("admin/user/add", cls.testUser0)
		cls.testReport["updatelevel_0.key"] = cls.testUser0["key"] = response["values"]["key"]
		response = cls.viur_api.add("admin/user/add", cls.testUser1)
		cls.testReport["updatelevel_1.key"] = cls.testUser1["key"] = response["values"]["key"]
		response = cls.viur_api.add("admin/user/add", cls.testUser2)
		cls.testReport["updatelevel_2.key"] = cls.testUser2["key"] = response["values"]["key"]

		# adding multiple users
		response = cls.viur_api.add("admin/user/add", cls.testUser3)
		cls.testUser3["key"] = response["values"]["key"]
		response = cls.viur_api.add("admin/user/add", cls.testUser4)
		cls.testUser4["key"] = response["values"]["key"]
		response = cls.viur_api.add("admin/user/add", cls.testUser5)
		cls.testUser5["key"] = response["values"]["key"]
		response = cls.viur_api.add("admin/user/add", cls.testUser6)
		cls.testUser6["key"] = response["values"]["key"]

		cls.testReport["updatelevel_3_multi.0.key"] = cls.testUser3["key"]
		cls.testReport["updatelevel_3_multi.1.key"] = cls.testUser6["key"]

		cls.testReport["updatelevel_4_multi.0.key"] = cls.testUser4["key"]
		cls.testReport["updatelevel_4_multi.1.key"] = cls.testUser6["key"]

		cls.testReport["updatelevel_5_multi.0.key"] = cls.testUser5["key"]
		cls.testReport["updatelevel_5_multi.1.key"] = cls.testUser6["key"]

		# adding report entry
		response = cls.viur_api.add("admin/report/add", cls.testReport)
		cls.reportChangedDates = [datetime.strptime(response["values"]["changedate"], "%d.%m.%Y %H:%M:%S")]
		cls.testReport["key"] = response["values"]["key"]
		time.sleep(6)

	@classmethod
	def tearDownClass(cls):
		# cls.viur_api.get("report/cleanup")
		super(UpdateLevelTest, cls).tearDownClass()

	def test00(self):
		"""Change testUser0.firstname. report refKeys and changedate should be updated

		:return:
		"""
		params = self.testUser0

		name, counter = params["firstname"].split()
		counter = int(counter) + 1
		params["firstname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(params["firstname"], status["relationList"][0]["dest.firstname"])
		self.assertEqual(params["firstname"], status["report"]["updatelevel_0.dest.firstname"])

	def test01(self):
		"""Change testUser0.lastname. report refKeys and changedate should not be updated

		:return:
		"""
		params = self.testUser0

		name, counter = params["lastname"].split()
		counter = int(counter) + 1
		params["lastname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(params["firstname"], status["relationList"][0]["dest.firstname"])

	def test02(self):
		"""Change testUser1.firstname. report refKeys and changedate should not be updated

		:return:
		"""

		params = self.testUser1

		name, counter = params["firstname"].split()
		counter = int(counter) + 1
		params["firstname_old"] = params["firstname"]
		params["firstname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][1]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][1]["lastname"])
		self.assertEqual(params["firstname_old"], status["relationList"][1]["dest.firstname"])
		self.assertEqual(params["firstname_old"], status["report"]["updatelevel_1.dest.firstname"])

	def test03(self):
		"""Change testUser1.lastname. report refKeys and changedate should not be updated

		:return:
		"""
		params = self.testUser1

		name, counter = params["lastname"].split()
		counter = int(counter) + 1
		params["lastname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][1]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][1]["lastname"])
		self.assertEqual(params["firstname_old"], status["relationList"][1]["dest.firstname"])
		self.assertEqual(params["firstname_old"], status["report"]["updatelevel_1.dest.firstname"])

	def test04(self):
		"""Change testUser2.firstname. report refKeys and changedate should not be updated

		:return:
		"""
		params = self.testUser2

		name, counter = params["firstname"].split()
		counter = int(counter) + 1
		params["firstname_old"] = params["firstname"]
		params["firstname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][2]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][2]["lastname"])
		self.assertEqual(params["firstname_old"], status["relationList"][2]["dest.firstname"])
		self.assertEqual(params["firstname_old"], status["report"]["updatelevel_2.dest.firstname"])

	def test05(self):
		"""Change testUser1.lastname. report refKeys and changedate should not be updated

		:return:
		"""
		params = self.testUser2

		name, counter = params["lastname"].split()
		counter = int(counter) + 1
		params["lastname"] = u"{0} {1}".format(name, counter)
		params = params.copy()
		params["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", params)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(params["firstname"], status["userList"][2]["firstname"])
		self.assertEqual(params["lastname"], status["userList"][2]["lastname"])
		self.assertEqual(params["firstname_old"], status["relationList"][2]["dest.firstname"])
		self.assertEqual(params["firstname_old"], status["report"]["updatelevel_2.dest.firstname"])

	def test06(self):
		"""Calling updateSearchIndex on report kind and check if all updateLevels are ok. report changedate should have changed

		:return:
		"""
		response = self.viur_api.get("report/callUpdateSearchIndex")
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(self.testUser0["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(self.testUser0["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(self.testUser1["firstname"], status["userList"][1]["firstname"])
		self.assertEqual(self.testUser1["lastname"], status["userList"][1]["lastname"])
		self.assertEqual(self.testUser2["firstname"], status["userList"][2]["firstname"])
		self.assertEqual(self.testUser2["lastname"], status["userList"][2]["lastname"])

		self.assertEqual(self.testUser0["firstname"], status["relationList"][0]["dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["relationList"][1]["dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["relationList"][2]["dest.firstname"])

		self.assertEqual(self.testUser0["firstname"], status["report"]["updatelevel_0.dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["report"]["updatelevel_1.dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["report"]["updatelevel_2.dest.firstname"])

	def test07(self):
		"""Changing firstname of testUser0 and check again

		:return:
		"""
		name, counter = self.testUser0["firstname"].split()
		counter = int(counter) + 1
		self.testUser0["firstname"] = u"{0} {1}".format(name, counter)
		self.testUser0["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser0)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(self.testUser0["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(self.testUser0["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(self.testUser0["firstname"], status["relationList"][0]["dest.firstname"])
		self.assertEqual(self.testUser0["firstname"], status["report"]["updatelevel_0.dest.firstname"])

	def test08(self):
		"""Calling updateSearchIndex on user kind.

		:return:
		"""
		self.viur_api.get("user/callUpdateSearchIndex")
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(self.testUser0["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(self.testUser0["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(self.testUser1["firstname"], status["userList"][1]["firstname"])
		self.assertEqual(self.testUser1["lastname"], status["userList"][1]["lastname"])
		self.assertEqual(self.testUser2["firstname"], status["userList"][2]["firstname"])
		self.assertEqual(self.testUser2["lastname"], status["userList"][2]["lastname"])

		self.assertEqual(self.testUser0["firstname"], status["relationList"][0]["dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["relationList"][1]["dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["relationList"][2]["dest.firstname"])

		self.assertEqual(self.testUser0["firstname"], status["report"]["updatelevel_0.dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["report"]["updatelevel_1.dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["report"]["updatelevel_2.dest.firstname"])

	def test09(self):
		"""Check if testUser3.firstname gets propagated to viur_relations and report entry in a multiple setting

		:return:
		"""
		name, counter = self.testUser3["firstname"].split()
		counter = int(counter) + 1
		self.testUser3["firstname"] = u"{0} {1}".format(name, counter)
		self.testUser3["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser3)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])

		self.assertEqual(self.testUser3["firstname"], status["userList"][3]["firstname"])
		self.assertEqual(self.testUser3["lastname"], status["userList"][3]["lastname"])
		self.assertEqual(self.testUser3["firstname"], status["relationList"][3]["dest.firstname"])
		updateLevel3_multi = [json.loads(i) for i in status["report"]["updatelevel_3_multi"]]
		self.assertEqual(self.testUser3["firstname"], updateLevel3_multi[0]["dest"]["firstname"])

	def test10(self):
		"""Check if testUser3.lastname does not change neither report nor viur relations

		:return:
		"""
		name, counter = self.testUser3["lastname"].split()
		counter = int(counter) + 1
		self.testUser3["lastname"] = u"{0} {1}".format(name, counter)
		self.testUser3["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser3)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(self.testUser3["firstname"], status["userList"][3]["firstname"])
		self.assertEqual(self.testUser3["lastname"], status["userList"][3]["lastname"])
		self.assertEqual(self.testUser3["firstname"], status["relationList"][3]["dest.firstname"])
		updateLevel3_multi = [json.loads(i) for i in status["report"]["updatelevel_3_multi"]]
		self.assertEqual(self.testUser3["firstname"], updateLevel3_multi[0]["dest"]["firstname"])

	def test11(self):
		"""Check if testUser4.firstname gets updated, but neither in vuir_relations nor in report.updatelevel4_multi

		:return:
		"""
		name, counter = self.testUser4["firstname"].split()
		counter = int(counter) + 1
		self.testUser4["firstname_old"] = self.testUser4["firstname"]
		self.testUser4["firstname"] = u"{0} {1}".format(name, counter)
		self.testUser4["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser4)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])

		self.assertEqual(self.testUser4["firstname"], status["userList"][4]["firstname"])
		self.assertEqual(self.testUser4["lastname"], status["userList"][4]["lastname"])
		self.assertEqual(self.testUser4["firstname_old"], status["relationList"][5]["dest.firstname"])
		updateLevel4_multi = [json.loads(i) for i in status["report"]["updatelevel_4_multi"]]
		self.assertEqual(self.testUser4["firstname_old"], updateLevel4_multi[0]["dest"]["firstname"])

	def test12(self):
		"""Check if testUser4.lastname gets updated, but neither in vuirRelations nor in report.updatelevel4_multi

		:return:
		"""
		name, counter = self.testUser4["lastname"].split()
		counter = int(counter) + 1
		self.testUser4["firstname"] = u"{0} {1}".format(name, counter)
		self.testUser4["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser4)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])

		self.assertEqual(self.testUser4["firstname"], status["userList"][4]["firstname"])
		self.assertEqual(self.testUser4["lastname"], status["userList"][4]["lastname"])
		self.assertEqual(self.testUser4["firstname_old"], status["relationList"][5]["dest.firstname"])
		updateLevel4_multi = [json.loads(i) for i in status["report"]["updatelevel_4_multi"]]
		self.assertEqual(self.testUser4["firstname_old"], updateLevel4_multi[0]["dest"]["firstname"])

	def test13(self):
		"""Check if testUser5.firstname gets updated, but neither in vuirRelations nor in report.updatelevel4_multi

		:return:
		"""
		name, counter = self.testUser5["firstname"].split()
		counter = int(counter) + 1
		self.testUser5["firstname_old"] = self.testUser5["firstname"]
		self.testUser5["firstname"] = u"{0} {1}".format(name, counter)
		self.testUser5["skey"] = self.viur_api.get_skey()
		self.viur_api.edit("admin/user/edit", self.testUser5)
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertEqual(self.reportChangedDates[-2], self.reportChangedDates[-1])

		self.assertEqual(self.testUser5["firstname"], status["userList"][5]["firstname"])
		self.assertEqual(self.testUser5["lastname"], status["userList"][5]["lastname"])
		self.assertEqual(self.testUser5["firstname_old"], status["relationList"][7]["dest.firstname"])
		updateLevel5_multi = [json.loads(i) for i in status["report"]["updatelevel_5_multi"]]
		self.assertEqual(self.testUser5["firstname_old"], updateLevel5_multi[0]["dest"]["firstname"])

	def test14(self):
		"""Check if updateSearchIndex updates testUser3 and testUser4 in viur_relations and report for multiple relational bones

		"""
		response = self.viur_api.get("report/callUpdateSearchIndex")
		time.sleep(6)
		status = self.viur_api.get("report/checkStatusJson")
		self.reportChangedDates.append(datetime.strptime(status["report"]["changedate"], "%Y.%m.%d %H:%M:%S"))
		self.assertLess(self.reportChangedDates[-2], self.reportChangedDates[-1])
		self.assertEqual(self.testUser0["firstname"], status["userList"][0]["firstname"])
		self.assertEqual(self.testUser0["lastname"], status["userList"][0]["lastname"])
		self.assertEqual(self.testUser1["firstname"], status["userList"][1]["firstname"])
		self.assertEqual(self.testUser1["lastname"], status["userList"][1]["lastname"])
		self.assertEqual(self.testUser2["firstname"], status["userList"][2]["firstname"])
		self.assertEqual(self.testUser2["lastname"], status["userList"][2]["lastname"])

		self.assertEqual(self.testUser0["firstname"], status["relationList"][0]["dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["relationList"][1]["dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["relationList"][2]["dest.firstname"])

		self.assertEqual(self.testUser0["firstname"], status["report"]["updatelevel_0.dest.firstname"])
		self.assertEqual(self.testUser1["firstname"], status["report"]["updatelevel_1.dest.firstname"])
		self.assertEqual(self.testUser2["firstname_old"], status["report"]["updatelevel_2.dest.firstname"])

		self.assertEqual(self.testUser3["firstname"], status["userList"][3]["firstname"])
		self.assertEqual(self.testUser3["lastname"], status["userList"][3]["lastname"])
		self.assertEqual(self.testUser4["firstname"], status["userList"][4]["firstname"])
		self.assertEqual(self.testUser4["lastname"], status["userList"][4]["lastname"])
		self.assertEqual(self.testUser5["firstname"], status["userList"][5]["firstname"])
		self.assertEqual(self.testUser5["lastname"], status["userList"][5]["lastname"])

		self.assertEqual(self.testUser3["firstname"], status["relationList"][3]["dest.firstname"])
		self.assertEqual(self.testUser4["firstname"], status["relationList"][5]["dest.firstname"])
		self.assertEqual(self.testUser5["firstname_old"], status["relationList"][7]["dest.firstname"])

		updateLevel3_multi = [json.loads(i) for i in status["report"]["updatelevel_3_multi"]]
		self.assertEqual(self.testUser3["firstname"], updateLevel3_multi[0]["dest"]["firstname"])
		updateLevel4_multi = [json.loads(i) for i in status["report"]["updatelevel_4_multi"]]
		self.assertEqual(self.testUser4["firstname"], updateLevel4_multi[0]["dest"]["firstname"])
		updateLevel5_multi = [json.loads(i) for i in status["report"]["updatelevel_5_multi"]]
		self.assertEqual(self.testUser5["firstname_old"], updateLevel5_multi[0]["dest"]["firstname"])


suite = unittest.TestLoader().loadTestsFromTestCase(UpdateLevelTest)
