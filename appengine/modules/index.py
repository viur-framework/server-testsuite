# -*- coding: utf-8 -*-

from server import exposed, conf
from server.render.html.default import Render


class index(Render):
	@exposed
	def index(self, *args, **kwargs):
		return self.getEnv().get_template("index.html").render(status=conf["viur.mainApp"].report.checkStatus())
