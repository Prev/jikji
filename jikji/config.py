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
from . import cprint


class ConfigPath :

	def __init__(self, sitepath, data) :
		self._sitepath = sitepath
		self._data = data


	@property
	def tpl(self):
		return "%s/%s" % (self._sitepath, self._data['path']['template'])
	

	@property
	def output(self):
		return "%s/%s" % (self._sitepath, self._data['path']['output'])


	@property
	def assets(self):
		asset_lists = self._data['path'].get('assets', [])
		return [ "%s/%s" % (self._sitepath, d) for d in asset_lists ]


	@property
	def pages_xml(self):
		return "%s/%s" % (self._sitepath, self._data['pages_xml'])


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
		self.path = ConfigPath(self.sitepath, self._config)
	

	@property
	def server_info(self) :
		return self._config['rest_server']




