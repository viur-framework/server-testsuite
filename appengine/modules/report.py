# -*- coding: utf-8 -*-
import json
import logging

from server import exposed, db, request
from server.skeleton import processChunk
from skeletons.user import userSkel
import json
__author__ = "Stefan Kögl <sk@mausbrand.de>"

from server.prototypes import List

from skeletons.report import ReportSkel


class Reports(List):
	viewTemplate = "mailshare_view"

	adminInfo = {
		"name": u"Reports",
		"handler": "list",
		"filter": {"orderby": "creationdate", "orderdir": "1"},
		"icon": "icons/modules/list.svg",
		"disableInternalPreview": True
	}

	def canView(self, skel):
		return True

	def _resolveSkelCls(self, *args, **kwargs):
		return ReportSkel

	def listFilter(self, rawFilter):
		return rawFilter

	@exposed
	def cleanup(self):
		[skel.delete() for skel in userSkel().all().filter("nick >=", "user").fetch()]
		[skel.delete() for skel in ReportSkel().all().fetch()]
		request.current.get().response.headers['content-type'] = 'application/json'
		return '"Ok"'

	@exposed
	def callUpdateSearchIndex(self):
		processChunk("report", None, None)
		return '"Ok"'

	@exposed
	def checkStatus(self):
		from pprint import pformat
		userList = list()

		for tmp in userSkel().all().filter("nick >", "user").order(("nick", db.ASCENDING)).run(limit=6):
			tmp = u"<li><pre>%s</pre></li>" % pformat(tmp, indent=4, width=80, depth=None)
			userList.append(tmp)

		updateList = db.Query("viur-relations").filter("viur_src_kind =", "report").order(("viur_src_property", db.ASCENDING)).run(limit=1000)
		tpl = u"<html><body><h3>Users</h3><ul>%s</ul><h3>Report Relations</h3><ul>%s</ul><h3>Report</h3><ul>%s</ul></body></html>"
		relationsList = list()
		for srcRel in sorted(updateList, key=lambda x: (x["viur_src_property"], x["dest.name"])):
			tmp = srcRel
			tmp = u"<li><pre>%s</pre></li>" % pformat(tmp, indent=4, width=80, depth=None)
			relationsList.append(tmp)

		reportList = list()
		for entry in db.Query("report").run(limit=100):
			reportList.append(u"<li><pre>%s</pre></li>" % pformat(entry, indent=4, width=80, depth=None))
		return tpl % (u"".join(userList), u"".join(relationsList), u"".join(reportList))

	@exposed
	def checkStatusJson(self):
		userList = list()

		for entry in userSkel().all().filter("nick >", "user").order(("nick", db.ASCENDING)).run(limit=10):
			entry["creationdate"] = entry["creationdate"].strftime("%Y.%m.%d %H:%M:%S")
			entry["changedate"] = entry["changedate"].strftime("%Y.%m.%d %H:%M:%S")
			userList.append(entry)

		updateList = db.Query("viur-relations").filter("viur_src_kind =", "report").order(("dest.firstname", db.ASCENDING)).run(limit=1000)
		relationsList = list()
		for entry in sorted(updateList, key=lambda x: (x["viur_src_property"], x["dest.name"])):
			relationsList.append(entry)

		reportList = db.Query("report").run(limit=1)
		entry = None
		if reportList:
			entry = reportList[0]
			entry["creationdate"] = entry["creationdate"].strftime("%Y.%m.%d %H:%M:%S")
			entry["changedate"] = entry["changedate"].strftime("%Y.%m.%d %H:%M:%S")

		request.current.get().response.headers['content-type'] = 'application/json'
		return json.dumps(
			{
				"userList": userList,
				"relationList": relationsList,
				"report": entry
			},
			indent=4
		)

Reports.json = True
