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

from .cprint import cprint


class Cache :

	def __init__(self, sitepath) :
		""" Init Cache Class with sitepath
		"""
		
		self.cachedir = os.path.join(sitepath, '.jikji', 'cache')
		os.makedirs(self.cachedir, exist_ok=True )


	def getpath(self, key) :
		""" Get cache file path of key
		"""
		return os.path.join(self.cachedir, quote_plus(key))


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


	def __init__(self, server_info, cache) :
		""" Init Model instance
		"""
		self.set_baseurl( server_info.get('base_url', '') )
		self.set_headers( server_info.get('headers', None) )
		self.cache = cache


	def set_baseurl(self, value) :
		if len(value) > 0 and value[-1] == '/' :
			value = value[0:-1]

		self._baseurl = value


	def get_baseurl(self) :
		return self._baseurl



	def set_headers(self, dictval) :
		if dictval is None :
			dictval = {}

		if dictval.get('Content-Type') is None :
			dictval['Content-Type'] = 'application/json'

		self._headers = dictval


	def get_headers(self) :
		return self._headers



	def geturl(self, api) :
		if api[0] != '/' :
			api = '/' + api
		return self.get_baseurl() + api



	def _rest(self, type, api, data=None, parsejson=True) :
		""" Rest Call to server
		:params
			- type: GET, POST, PUT, or DELETE
			- api: api string appended to baseurl
			- data: url form data (default: None)

		:return json-parsed object
		"""

		cprint.write("%s '%s' " % (type.upper(), api))

		if data is not None :
			data = json.dumps(data)


		# Call proper method of requests (maybe GET, POST or ext)
		r = getattr(requests, type.lower())(
			url = self.geturl(api),
			data = data,
			headers = self.get_headers()
		)

		try :
			r.raise_for_status()

		except requests.exceptions.HTTPError as e :
			# Raise ModelException when error occurs
			# Generater will handle Error and stop generating
			me = ModelException(HTTPError=e)
			cprint.error('%s' % me.status)
			raise me

		


		if parsejson :
			result = r.json()
		else :
			result = r.text
		
		cprint.ok('finish')
		return result


	def get(self, api, data=None, immutable=False) :
		""" Send a GET request to REST Sever
		:params
			- api: api string
			- data: url form data (default: None)
			- immutable: if immutable, make cache with key of api url (default: False)

		:return json-parsed object
		"""

		url = self.geturl(api)

		# If immutable, use cache
		if immutable == True :
			cachedata = self.cache.get(url)
			if cachedata is not None :
				cprint.write("GET '%s' " % api)
				cprint.ok('finish (use cache)')
				return cachedata


		result = self._rest('GET', api, data)

		if immutable == True :
			self.cache.set(url, result)

		return result



	def post(self, api, data=None) :
		""" Send a POST request to REST Sever
		:params
			- api: api string
			- data: url form data (default: None)

		:return json-parsed object
		"""
		return self._rest('POST', api, data)



	def put(self, api, data=None) :
		""" Send a PUT request to REST Sever
		:params
			- api: api string
			- data: url form data (default: None)

		:return json-parsed object
		"""
		return self._rest('PUT', api, data)



	def delete(self, api, data=None) :
		""" Send a DELETE request to REST Sever
		:params
			- api: api string
			- data: url form data (default: None)

		:return json-parsed object
		"""
		return self._rest('DELETE', api, data)





class ModelException(Exception) :

	def __init__(self, HTTPError) :
		code = HTTPError.response.status_code
		status_msg = requests.status_codes._codes[code][0].replace('_', ' ').upper()

		self.HTTPError = HTTPError
		self.status = '%s %s' % (code, status_msg)


