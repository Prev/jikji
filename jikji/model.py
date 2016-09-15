# -*- coding: utf-8 -*-
"""
	jikji/model
	----------------
	Connect with Rest-Server

	:author: Prev(prevdev@gmail.com)
"""

import urllib.request
import urllib.error
import base64
import json


class Model :

	"""
	Init Model instance
	"""
	def __init__(self, rest_server_info) :
		self.set_baseurl( rest_server_info['base_url'] )
		self.set_headers( rest_server_info.get('headers', {}) )


	"""
	Getter / Setter of baseurl
	"""
	def set_baseurl(self, value) :
		if value[-1] == '/' :
			value = value[0:-1]

		self._baseurl = value

	def get_baseurl(self) :
		return self._baseurl


	"""
	Getter / Setter of baseurl
	"""
	def set_headers(self, value) :
		if value is None :
			value = {}

		self._headers = value

	def get_headers(self) :
		return self._headers



	"""
	Get data from Rest Server
	@params
		- api: api string (document id or predefined api like '_all_docs')
		- data: url form data (default: None)
	@return json-parsed object
	"""

	def get(self, api, data=None) :
		if api[0] != '/' :
			api = '/' + api

		url = self.get_baseurl() + api
		req = urllib.request.Request(url, data, self.get_headers())

		try :
			with urllib.request.urlopen(req) as response:
				page = response.read()

		except urllib.error.HTTPError as err :
			if err.code == 404 :
				print('404 Error on "%s"' % url)


		page = page.decode('utf-8')
		data = json.loads(page)

		return data


