#-*- coding: utf-8 -*-

"""
Jikji/Model
@author Prev(prevdev@gmail.com)

Model
Connect with Rest-Server

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
		self.base_url = rest_server_info['base_url']
		self.headers = rest_server_info['headers']


		if self.base_url[-1] == '/' :
			self.base_url = self.base_url[0:-1]
	
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

		url = self.base_url + api
		req = urllib.request.Request(url, data, self.headers)
		
		try :
			with urllib.request.urlopen(req) as response:
				page = response.read()

		except urllib.error.HTTPError as err :
			if err.code == 404 :
				print('404 Error on "%s"' % url)


		page = page.decode('utf-8')
		data = json.loads(page)

		return data


