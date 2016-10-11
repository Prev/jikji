# -*- coding: utf-8 -*-
"""
	jikji/model
	----------------
	Connect with Rest-Server

	:author: Prev(prevdev@gmail.com)
"""

import requests
import base64
import json
import os

from .cprint import cprint


class Model :

	__attrs__ =[
		'cache', '_default_baseurl', '_default_headers', '_macros'
	]


	def __init__(self, server_info, cache) :
		""" Init Model instance
		"""
		self.set_default_baseurl( server_info.get('baseurl', '') )
		self.set_default_headers( server_info.get('headers', None) )
		self.cache = cache

		self._macros = {}



	def _filter_baseurl(self, baseurl) :
		""" Remove last char if it is '/'
		"""
		if len(baseurl) > 0 and baseurl[-1] == '/' :
			baseurl = baseurl[0:-1]

		return baseurl



	def set_default_baseurl(self, value) :
		""" Set default baseurl (like host)
			Remove last char if it is '/'
		"""
		self._default_baseurl = self._filter_baseurl(value)


	def get_default_baseurl(self) :
		""" Get default baseurl
		"""
		return self._default_baseurl




	def set_default_headers(self, dictval) :
		""" Set default headrs
			Append Content-Type to application/json
		"""
		if dictval is None :
			dictval = {}

		if dictval.get('Content-Type') is None :
			dictval['Content-Type'] = 'application/json'

		self._default_headers = dictval


	def get_default_headers(self) :
		""" Get default headers
		"""
		return self._default_headers


	def get_headers(self, headers=None) :
		""" Return default_headers if param 'headers' is None,
			else return headers
		"""
		if headers is not None :
			return headers
		else :
			return self.get_default_headers()



	def geturl(self, api, baseurl=None) :
		""" Get full url combining with api and baseurl
		"""
		if api[0] != '/' :
			api = '/' + api

		if baseurl is not None: 
			return self._filter_baseurl(baseurl) + api
		else :
			return self.get_default_baseurl() + api



	def _rest(self, method, api, data=None, baseurl=None, headers=None, parsejson=True) :
		""" Rest Call to server
		:params
			- method: GET, POST, PUT, or DELETE
			- api: api string appended to baseurl
			- data: url form data (default: None)
			- baseurl: baseurl of api (default: jikji.Config.server_info.baseurl)
			- headers: headers in http call (default: jikji.Config.server_info.headers)
			- parsejson = boolean status of parsing result to json (default: True)

		:return json-parsed object
		"""

		url = self.geturl(api, baseurl)

		if data is not None :
			data = json.dumps(data)
			

		cprint.write("%s '%s' "% (method.upper(), (api if (baseurl is None) else url) ))

		# Call proper method of requests (maybe GET, POST or ext)
		r = getattr(requests, method.lower())(
			url = url,
			data = data,
			headers = self.get_headers(headers)
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


	def get(self, api, data=None, baseurl=None, headers=None, immutable=False) :
		""" Send a GET request to REST Sever
		:params
			- api: api string
			- data: url form data (default: None)
			- baseurl: baseurl of api (default: jikji.Config.server_info.baseurl)
			- headers: headers in http call (default: jikji.Config.server_info.headers)
			- immutable: if immutable, make cache with key of api url (default: False)

		:return json-parsed object
		"""

		url = self.geturl(api, baseurl)

		# If immutable, use cache
		if immutable == True :
			cachedata = self.cache.get(url)
			if cachedata is not None :
				cprint.write("GET '%s' " % api)
				cprint.ok('finish (use cache)')
				return cachedata


		result = self._rest('GET', api, data, baseurl, headers)

		if immutable == True :
			self.cache.set(url, result)

		return result



	def post(self, api, data=None, baseurl=None, headers=None) :
		""" Send a POST request to REST Sever
		:params: (same with self.post)
		:return: json-parsed object
		"""
		return self._rest('POST', api, data, baseurl, headers)



	def put(self, api, data=None, baseurl=None, headers=None) :
		""" Send a PUT request to REST Sever
		:params: (same with self.post)
		:return: json-parsed object
		"""
		return self._rest('PUT', api, data, baseurl, headers)



	def delete(self, api, data=None, baseurl=None, headers=None) :
		""" Send a DELETE request to REST Sever
		:params: (same with self.post)
		:return: json-parsed object
		"""
		return self._rest('DELETE', api, data, baseurl, headers)



	def make_macro(self, name, method, api, data=None, baseurl=None, headers=None, immutable=False) :
		""" Make macro of model
		:params
			- name: name of macro, call macro by this value
			- method: method of macro
			- api: api string on request
				special string "$n" will be replaced with *args in `self.macro`
				ex) '/_design/$1/_view/$2'

			- **others: (sname with self.get)
		"""

		self._macros[name] = {
			'method' : method,
			'api'    : api,
			'data'   : data,
			'baseurl': baseurl,
			'headers': headers,
			'immutable': immutable
		}


	def macro(self, name, *args) :
		""" Call macro of model
		:params
			- name: name of macro
			- *args: replacing string in api
		"""

		cur_macro = self._macros[name]

		method = cur_macro['method']
		api = cur_macro['api']

		for index, arg in enumerate(args):
			api = api.replace('$%d' % (index+1), arg)

		kwarg = {
			'api'       : api,
			'data'      : cur_macro['data'],
			'baseurl'   : cur_macro['baseurl'],
			'headers'   : cur_macro['headers']
		}

		if method.upper() == 'GET' :
			kwarg['immutable'] = cur_macro['immutable']
			return self.get(**kwarg)

		else :
			kwarg['method'] = method
			return self._rest(**kwarg)



class ModelException(Exception) :

	def __init__(self, HTTPError) :
		code = HTTPError.response.status_code
		status_msg = requests.status_codes._codes[code][0].replace('_', ' ').upper()

		self.HTTPError = HTTPError
		self.status = '%s %s' % (code, status_msg)


