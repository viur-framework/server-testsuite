# -*- coding: utf-8 -*-

from server.bones.passwordBone import passwordBone
from server.bones.stringBone import stringBone
from server.modules.user import userSkel


class userSkel(userSkel):
	nick = stringBone(descr=u"nick", required=True, indexed=True, searchable=True)
	firstname = stringBone(descr=u"Vorname", required=True, indexed=True, searchable=True)
	lastname = stringBone(descr=u"Nachname", required=True, indexed=True, searchable=True)
	password = passwordBone(descr="Password", required=False, readOnly=False, visible=True)
