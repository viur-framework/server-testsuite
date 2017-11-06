# -*- coding: utf-8 -*-
from server import exposed
from server.modules.user import User, UserPassword
from server.skeleton import processChunk
from skeletons.user import userSkel


class user(User):
	baseSkel = userSkel
	viewSkel = userSkel

	authenticationProviders = [UserPassword]
	validAuthenticationMethods = [(UserPassword, None)]

	adminInfo = {
		"name": u"Nutzer",
		"handler": "list",
		"icon": "icons/modules/contactperson.svg",
		"disableInternalPreview": True
	}

	@exposed
	def callUpdateSearchIndex(self):
		processChunk("user", None, None)
		return '"Ok"'
