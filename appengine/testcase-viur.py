# -*- coding: utf-8 -*-
# !/usr/bin/python

import os

from server import utils
from server.config import conf

conf["admin.vi.name"] = "Testcase"

import modules
import server

from server import securityheaders

securityheaders.addCspRule("default-src", "self", "enforce")  # enforce

securityheaders.addCspRule("script-src", "self", "enforce")
securityheaders.addCspRule("script-src", "ajax.googleapis.com", "enforce")
securityheaders.addCspRule("script-src", "www.google-analytics.com", "enforce")
securityheaders.addCspRule("script-src", "maps.googleapis.com", "enforce")
securityheaders.addCspRule("script-src", "maps.google.de", "enforce")
securityheaders.addCspRule("script-src", "maps.gstatic.de", "enforce")
securityheaders.addCspRule("script-src", "maps.gstatic.com", "enforce")
securityheaders.addCspRule("script-src", "unsafe-eval", "enforce")
securityheaders.addCspRule("script-src", "unsafe-inline", "enforce")

securityheaders.addCspRule("img-src", "self", "enforce")
securityheaders.addCspRule("img-src", "*.ggpht.com", "enforce")
securityheaders.addCspRule("img-src", "*.googleusercontent.com", "enforce")
securityheaders.addCspRule("img-src", "*.g.doubleclick.net", "enforce")
securityheaders.addCspRule("img-src", "www.google-analytics.com", "enforce")
securityheaders.addCspRule("img-src", "www.google.com", "enforce")
securityheaders.addCspRule("img-src", "www.google.de", "enforce")
securityheaders.addCspRule("img-src", "csi.gstatic.com", "enforce")
securityheaders.addCspRule("img-src", "unsafe-inline", "enforce")
securityheaders.addCspRule("img-src", "data:", "enforce")

securityheaders.addCspRule("font-src", "self", "enforce")
securityheaders.addCspRule("font-src", "fonts.gstatic.com", "enforce")
securityheaders.addCspRule("font-src", "unsafe-inline", "enforce")
securityheaders.addCspRule("font-src", "data:", "enforce")

securityheaders.addCspRule("style-src", "self", "enforce")
securityheaders.addCspRule("style-src", "fonts.googleapis.com", "enforce")
securityheaders.addCspRule("style-src", "unsafe-inline", "enforce")

# securityheaders.addCspRule("style-src","hello.myfonts.net","enforce") #Noop!

securityheaders.addCspRule("frame-src", "self", "enforce")
securityheaders.addCspRule("frame-src", "www.youtube-nocookie.com", "enforce")
securityheaders.addCspRule("frame-src", "www.youtube.com", "enforce")
securityheaders.addCspRule("frame-src", "docs.google.com", "enforce")
securityheaders.addCspRule("frame-src", "maps.google.de", "enforce")
securityheaders.addCspRule("frame-src", "www.google.com", "enforce")
securityheaders.addCspRule("frame-src", "drive.google.com", "enforce")
securityheaders.addCspRule("frame-src", "accounts.google.com", "enforce")

server.setDefaultLanguage("de")
application = server.setup(modules)


conf["viur.availableLanguages"] = ["de"]
conf["viur.defaultLanguage"] = "de"
conf["viur.languageMethod"] = "url"
conf["viur.forceSSL"] = True

conf["viur.db.caching"] = 0
conf["viur.debug.traceQueries"] = True
conf["viur.debug.traceExternalCallRouting"] = True
conf["viur.debug.traceInternalCallRouting"] = True


def main():
	server.run()


if __name__ == '__main__':
	main()
