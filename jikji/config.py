# -*- coding: utf-8 -*-
"""
	jikji/config
	---------------
	Config Manage Class

	:author: Prev(prevdev@gmail.com)
"""

import os
import sys
import json
from .cprint import cprint


class ConfigPath :
	""" ConfigPath Object
		'path' property in config.json data
	"""

	_defaults = {
		'template': 'templates',
		'output': 'output',
		'assets': [],
		'pages_xml': 'pages.xml'
	}


	def __init__(self, sitepath, data) :
		""" Init ConfigPath Instance
		"""
		self.sitepath = sitepath
		self._data = data


	def _get(self, key) :
		""" Get data form _data with default value
		"""
		global _defaults
		return self._data.get(key, self._defaults[key]) # get value in dict with default value


	@property
	def tpl(self):
		return os.path.join(self.sitepath, self._get('template'))
	

	@property
	def output(self):
		return os.path.join(self.sitepath, self._get('output'))


	@property
	def assets(self):
		asset_lists = self._get('assets')
		return [ os.path.join(self.sitepath, d) for d in asset_lists ]


	@property
	def pages_xml(self):
		return os.path.join(self.sitepath, self._get('pages_xml'))



class Config :
	
	def __init__(self, config_file_path) :
		if os.path.isdir(config_file_path) :
			config_file_path += '/config.json'

		try :
			config_file = open(config_file_path, 'r')
			
		except FileNotFoundError :
			cprint.error('Error on jikji.Config.__init__')
			cprint.bold('Config file "%s" NOT FOUND' % config_file_path)
			sys.exit(-1)



		config_data = config_file.read()

		self._config = json.loads(config_data)
		self.sitepath = os.path.dirname(config_file_path)

		self._path_instance = ConfigPath(
			sitepath = self.sitepath,
			data = self._config.get('path', {})
		)


	@property
	def path(self):
		return self._path_instance
	
	
	@property
	def server_info(self) :
		return self._config.get('server_info', {})


	@property
	def log_history(self):
		return self._config.get('log_history', False)
	

	@property
	def imports(self) :
		return self._config.get('imports', [])




