# -*- coding: utf-8 -*-
"""
	jikji/model
	----------------
	Connect with Rest-Server

	:author: Prev(prevdev@gmail.com)
"""

from urllib.parse import quote_plus
import urllib.request
import urllib.error
import base64
import json
import os


class Cache :

	"""
	Init Cache Class with site_path
	"""
	def __init__(self, sitepath) :
		cachedir = sitepath + '/.jikji/cache/'
		os.makedirs(cachedir, exist_ok=True )

		self.cachedir = cachedir


	"""
	Get cache file path of key
	"""
	def getpath(self, key) :
		return self.cachedir + quote_plus(key)


	"""
	Get cached data with key
	If cache not found, return default value of param (default: None)
	"""
	def get(self, key, default=None) :
		path = self.getpath(key)
		
		if os.path.isfile(path) :
			with open(path, 'r') as file:
				content = file.read()

			return json.loads(content)

		else :
			return default

	"""
	Set cache data with key, value
	"""
	def set(self, key, value) :
		path = self.getpath(key)
		
		with open(path, 'w') as file:
			file.write( json.dumps(value) )



class Model :
	"""
	Init Model instance
	"""
	def __init__(self, rest_server_info, cache) :
		self.set_baseurl( rest_server_info['base_url'] )
		self.set_headers( rest_server_info.get('headers', {}) )
		self.cache = cache


	"""
	Getter/Setter of baseurl
	"""
	def set_baseurl(self, value) :
		if value[-1] == '/' :
			value = value[0:-1]

		self._baseurl = value

	def get_baseurl(self) :
		return self._baseurl


	"""
	Getter/Setter of baseurl
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
		- immutable: if immutable, make cache with key of api url (default: False)

	@return json-parsed object
	"""

	def get(self, api, data=None, immutable=False) :
		if api[0] != '/' :
			api = '/' + api
		url = self.get_baseurl() + api


		if immutable == True :
			cachedata = self.cache.get(url)
			if cachedata is not None :
				return cachedata


		req = urllib.request.Request(url, data, self.get_headers())
		try :
			with urllib.request.urlopen(req) as response:
				page = response.read()

		except urllib.error.HTTPError as err :
			if err.code == 404 :
				cprint.error('404 Error on "%s"' % url)


		page = page.decode('utf-8')
		result = json.loads(page)


		if immutable == True :
			self.cache.set(url, result)

		return result


