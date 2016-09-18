# -*- coding: utf-8 -*-
"""
	jikji/model
	----------------
	Connect with Rest-Server

	:author: Prev(prevdev@gmail.com)
"""

from urllib.parse import quote_plus
import requests
import base64
import json
import os
from . import cprint


class Cache :

	def __init__(self, sitepath) :
		""" Init Cache Class with site_path
		"""
		cachedir = sitepath + '/.jikji/cache/'
		os.makedirs(cachedir, exist_ok=True )

		self.cachedir = cachedir


	def getpath(self, key) :
		""" Get cache file path of key
		"""
		return self.cachedir + quote_plus(key)


	def get(self, key, default=None) :
		""" Get cached data with key
		If cache not found, return default value of param (default: None)
		"""
		path = self.getpath(key)
		
		if os.path.isfile(path) :
			with open(path, 'r') as file:
				content = file.read()

			return json.loads(content)

		else :
			return default


	def set(self, key, value) :
		""" Set cache data with key, value
		"""
		path = self.getpath(key)
		
		with open(path, 'w') as file:
			file.write( json.dumps(value) )



class Model :

	__attrs__ =[
		'cache', '_baseurl', '_headers'	
	]


	def __init__(self, rest_server_info, cache) :
		""" Init Model instance
		"""
		self.set_baseurl( rest_server_info['base_url'] )
		self.set_headers( rest_server_info.get('headers', None) )
		self.cache = cache


	def set_baseurl(self, value) :
		if value[-1] == '/' :
			value = value[0:-1]

		self._baseurl = value

	def get_baseurl(self) :
		return self._baseurl



	def set_headers(self, value) :
		if value is None :
			value = {}

		self._headers = value

	def get_headers(self) :
		return self._headers




	def get(self, api, data=None, immutable=False) :
		""" Get data from Rest Server
		:params
			- api: api string (document id or predefined api like '_all_docs')
			- data: url form data (default: None)
			- immutable: if immutable, make cache with key of api url (default: False)

		:return json-parsed object
		"""

		# Api URL validating
		if api[0] != '/' :
			api = '/' + api
		url = self.get_baseurl() + api

		cprint.write("GET '%s'.. " % api)


		# If immutable, use cache
		if immutable == True :
			cachedata = self.cache.get(url)
			if cachedata is not None :
				cprint.ok('finish (use cache)')
				return cachedata


		# Raise ModelException when error occurs
		# Generater will handle Error and stop generating
		r = requests.get(url, data=data, headers=self.get_headers())
		try :
			r.raise_for_status()

		except requests.exceptions.HTTPError as e :
			me = ModelException(HTTPError=e)
			cprint.error('%s' % me.status)

			raise me


		result = r.json()
		cprint.ok('finish')

		if immutable == True :
			self.cache.set(url, result)

		return result


class ModelException(Exception) :

	def __init__(self, HTTPError) :
		code = HTTPError.response.status_code
		status_msg = requests.status_codes._codes[code][0].replace('_', ' ').upper()

		self.HTTPError = HTTPError
		self.status = '%s %s' % (code, status_msg)


