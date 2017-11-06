# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import json
import os
import os.path
import shutil
import time
from urllib import quote

import requests
from celery.utils.log import get_task_logger
from ConfigParser import SafeConfigParser
from requests_toolbelt import MultipartEncoder

log = get_task_logger(__name__)


class ViurInterface(object):
	def __init__(self):
		super(ViurInterface, self).__init__()
		config = SafeConfigParser()
		config.readfp(open("credentials.ini"), "credentials.ini")
		self.username = config.get("server-testsuite-viur", "username")
		self.password = config.get("server-testsuite-viur", "password")
		self.base_url = config.get("server-testsuite-viur", "base_url")
		self.session = requests.Session()

	def login_viur_master(self):
		response = self.session.post(
			"{0}/{1}".format(self.base_url, "admin/user/login"),
			data={
				"name": self.username,
				"password": self.password,
				"skey": self.get_skey()
			})
		# print response.text
		if response.status_code not in (200, 302):
			log.error(response.status_code)
			log.error(response.text)
			log.error("Login nicht erfolgreich!")

	def login(self):
		response = self.session.post(
			"{0}/{1}".format(self.base_url, "admin/user/auth_userpassword/login"),
			data={
				"name": self.username,
				"password": self.password,
				"skey": self.get_skey()
			})
		# print response.text
		if response.status_code not in (200, 302):
			log.error(response.status_code)
			log.error(response.text)
			log.error("Login nicht erfolgreich!")

	def logout(self):
		response = self.session.get(
			"{0}/{1}".format(self.base_url, "admin/user/logout"),
			params={
				"skey": self.get_skey()
			})
		if response.status_code != 200:
			log.error(response.status_code)
			log.error(response.text)
			log.error("Logout nicht erfolgreich!")

	def get_skey(self):
		return self.session.get("%s/%s" % (self.base_url, "admin/skey")).json()

	def add(self, url, params):
		"""
		:param url: url
		:type url: str
		:param params: get params
		:type params: dict
		:return: dict
		"""
		url = url.lstrip("/")
		mypath = "%s/%s" % (self.base_url, url)
		response = self.session.post(mypath, data=params)
		if response.status_code != 200:
			raise ValueError(response)

		answer = response.json()
		if answer["action"] != "addSuccess":
			errcount = False
			for bone in answer["structure"]:
				if bone[1]["error"]:
					print(repr(bone[0]), repr(bone[1]["error"]))
					errcount = True
			if errcount:
				raise Exception()
		return answer

	def edit(self, url, data):
		"""
		:param url: url
		:type url: str
		:param data: get data
		:type params: dict
		:return: dict
		"""
		url = url.lstrip("/")
		mypath = "%s/%s" % (self.base_url, url)
		response = self.session.post(mypath, data=data)
		if response.status_code != 200:
			raise ValueError(response)

		answer = response.json()
		if answer["action"] != "editSuccess":
			errcount = False
			for bone in answer["structure"]:
				if bone[1]["error"]:
					log.error(bone[0], bone[1]["error"])
					errcount = True
			if errcount:
				raise Exception()
		return answer

	def get(self, url, params=None):
		"""

		:param url: url
		:type url: str
		:param params: get params
		:type params: dict
		:return:
		"""
		url = url.lstrip("/")
		mypath = "%s/%s" % (self.base_url, url)
		response = self.session.get(mypath, params=params)
		if response.status_code != 200:
			log.error(response.status_code)
			log.error(response.text)
			return None
		answer = response.json()
		return answer

	def get_list(self, url, params=None):
		"""

		:param url: url
		:type url: str
		:param params: get params
		:type params: dict
		:return:
		"""
		url = url.lstrip("/")
		mypath = "%s/%s" % (self.base_url, url)
		if params is None:
			params = dict()
		params.setdefault("amount", "99")
		skellist = list()
		structure = None
		while 1:
			response = self.session.get(mypath, params=params)
			if response.status_code != 200:
				log.error("get list on, status code: %r, text: %r", response.status_code, response.text)
				return None

			answer = response.json()
			cursor = answer["cursor"]
			items = answer["skellist"]
			if items:
				skellist.extend(items)

			if structure is None:
				structure = answer.get("structure")

			if not items or not cursor:
				break

			params["cursor"] = cursor

		return structure, skellist

	def download_file(self, src_module, src_dlkey, temp_filename):
		response = self.session.get(
			u"{0}/{1}/download/{2}?download=1".format(self.base_url, src_module, quote(src_dlkey)), stream=True)
		newfile = open(temp_filename, "wb")
		shutil.copyfileobj(response.raw, newfile)
		newfile.flush()
		os.fsync(newfile.fileno())
		newfile.close()
		del newfile
		del response
		time.sleep(0.2)

	def upload_file(self, upload_module, temp_filename, dest_filename, mimetype, payload, key_name="key"):
		"""

		:param image_entry: the representation of the file to upload
		:type image_entry: dict
		:return: dict
		"""

		response = self.session.get(
			"{0}/json/{1}/getUploadURL".format(self.base_url, upload_module),
			params={"skey": self.get_skey()})
		upload_url = response.content
		dest_filename = base64.urlsafe_b64encode(dest_filename.encode("utf-8"))
		for key, value in payload.iteritems():
			if not isinstance(value, basestring):
				payload[key] = str(value)
		data = {}
		with open(temp_filename, "rb") as myFile:
			payload["FileData"] = (dest_filename, myFile, mimetype, {'Expires': '0'})
			encoder = MultipartEncoder(payload)
			data = self.session.post(
				upload_url,
				data=encoder,
				headers={'Content-Type': encoder.content_type}
			)
		dataJson = data.json()
		fileKey = dataJson["values"][0][key_name]
		return fileKey

	def upload_file_old(self, image_entry):
		"""

		:param image_entry: the representation of the file to upload
		:type image_entry: dict
		:return: dict
		"""

		local_filename = image_entry["temp_filename"]
		parent_node_key = image_entry["upload"]["dest_parent_node_key"]
		dest_filename = image_entry["dest_filename"]
		data = open(local_filename, "rb").read()
		response = self.session.get(
			self.base_url + "/admin/file/getUploadURL",
			params={"skey": self.get_skey()})
		upload_url = response.content
		myfilename = base64.urlsafe_b64encode(dest_filename)
		metadata = image_entry.get("metadata", "")
		if metadata:
			metadata = json.dumps(metadata)
		myfiles = {"FileData": (myfilename, data, image_entry["dest_mimetype"], {'Expires': '0'})}
		skel = self.session.post(
			upload_url, data={
				"node": parent_node_key,
				"height": str(image_entry["dest_height"]),
				"width": str(image_entry["dest_width"]),
				"metadata": metadata,
				"colorspace": image_entry.get("dest_colorspace", "sRGB"),
				"dpi": image_entry.get("dest_density", 72)
			},
			files=myfiles)
		skel = skel.json()["values"][0]
		image_entry["upload"]["dest_file_key"] = skel["key"]
		return image_entry

	def set_image_2_media(self, image_entry):
		dest_key = image_entry["attach_key"]
		dest_module = image_entry["attach_module"]
		dest_file_key = image_entry["dest_file_key"]
		dest_bone_name = image_entry["attach_bone_name"]
		metadata = image_entry.get("src_metadata", "")
		if metadata:
			log.debug("metah: %r", type(metadata))
		response = self.session.post(
			"{0}/{1}/setfile".format(self.base_url, dest_module),
			data={
				"dest_key": dest_key,
				"dest_file_key": dest_file_key,
				"dest_bone_name": dest_bone_name,
				"src_colorspace": image_entry.get("src_colorspace", "sRGB"),
				"dest_colorspace": image_entry.get("dest_colorspace", "sRGB"),
				"dpi": image_entry.get("src_density", 72),
				"metadata": metadata})
		try:
			response = response.json()
			log.debug("set_image_2_media response: %r", response)
		except Exception as err:
			log.exception(err)
		return image_entry

	def attach_previews(self, attach_module, attach_key, lowres_key=None, highres_key=None, **kwargs):
		data = {
			"media_key": attach_key,
			"lowres_key": lowres_key,
			"highres_key": highres_key,
		}
		data.update(kwargs)
		response = self.session.post(
			"{0}/{1}/attach_previews".format(self.base_url, attach_module),
			data=data
		)
		try:
			response = response.json()
			log.debug("attach_previews response: %r", response)
		except Exception as err:
			log.exception(err)

	def append_image_2_media(self, image_entry):
		dest_key = image_entry["attach_key"]
		dest_file_key = image_entry["dest_file_key"]
		dest_module = image_entry["attach_module"]
		response = self.session.post(
			"{0}/{1}/appendfile".format(self.base_url, dest_module),
			data={
				"dest_key": dest_key,
				"dest_file_key": dest_file_key,
				"dest_bone_name": image_entry["attach_bone_name"],
				"src_colorspace": image_entry.get("src_colorspace", "sRGB"),
				"dest_colorspace": image_entry.get("dest_colorspace", "sRGB"),
				"dpi": image_entry.get("src_density", 72),
				"metadata": None
			}
		)
		try:
			response.json()
		except Exception as err:
			log.exception(err)
		return image_entry

	def recursiveDownloader(self, repoKey, directoryParams=None, fileParams=None, directory=None):
		directoryQuery = "{0}/json/file/list/node/{1}".format(self.base_url, repoKey)
		fileQuery = "{0}/json/file/list/leaf/{1}".format(self.base_url, repoKey)
		if directoryParams is None:
			directoryParams = dict()
		directoryParams.setdefault("amount", "99")

		if fileParams is None:
			fileParams = dict()
		fileParams.setdefault("amount", "99")

		if directory is None:
			directory = {"repoKey": repoKey, "files": list(), "directories": list()}

		while 1:
			response = self.session.get(directoryQuery, params=directoryParams)
			if response.status_code != 200:
				pass
				log.error("get directory list %r, status code: %r, text: %r", directory, response.status_code,
				          response.text)
				return None

			answer = response.json()
			directoryItems = answer["skellist"]

			directoryParams["cursor"] = answer["cursor"]
			for subDirectory in directoryItems:
				subDirectory["files"] = list()
				subDirectory["directories"] = list()
				directory["directories"].append(subDirectory)
				self.recursiveDownloader(subDirectory["id"], directory=subDirectory)

			response = self.session.get(fileQuery, params=fileParams)
			if response.status_code != 200:
				log.error("get file list on %r, status code: %r, text: %r", directory, response.status_code,
				          response.text)
				return None

			answer = response.json()
			fileItems = answer["skellist"]
			if not fileItems and not directoryItems:
				break

			fileParams["cursor"] = answer["cursor"]
			directory["files"].extend(fileItems)

		return directory
