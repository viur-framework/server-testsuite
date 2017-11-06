# -*- coding: utf-8 -*-
__author__ = "Stefan Kögl <sk@mausbrand.de>"

from server.bones.userBone import userBone
from server.skeleton import Skeleton


class ReportSkel(Skeleton):
	kindName = "report"
	searchIndex = "report"

	updatelevel_0 = userBone(
		descr=u"Nutzer 0",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=0
	)

	updatelevel_1 = userBone(
		descr=u"Nutzer 1",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=1
	)

	updatelevel_2 = userBone(
		descr=u"Nutzer 2",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=2
	)

	updatelevel_3_multi = userBone(
		descr=u"Nutzer 0",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=0,
		multiple=True
	)

	updatelevel_4_multi = userBone(
		descr=u"Nutzer 1",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=1,
		multiple=True
	)

	updatelevel_5_multi = userBone(
		descr=u"Nutzer 2",
		indexed=True,
		required=True,
		searchable=True,
		refKeys=["key", "name", "firstname"],
		updateLevel=2,
		multiple=True
	)
