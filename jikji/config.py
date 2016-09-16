# -*- coding: utf-8 -*-
"""
	jikji/config
	---------------
	Config Manage Class

	:author: Prev(prevdev@gmail.com)
"""

import os
import os.path
import sys
import json
from . import cprint

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

		self.site_path = os.path.dirname(config_file_path)
		self.config = json.loads(config_data)


	def tpl_dir(self) :
		return "%s/%s" % (self.site_path, self.config['path']['template'])


	def output_dir(self) :
		return "%s/%s" % (self.site_path, self.config['path']['output'])


	def pages_xml_path(self) :
		return "%s/%s" % (self.site_path, self.config['pages_xml'])


	def rest_server_info(self) :
		return self.config['rest_server']

