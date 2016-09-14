#-*- coding: utf-8 -*-

"""
Jikji/config
@author Prev(prevdev@gmail.com)


Config Manage Class
"""

import os
import json

class Config :
	
	def __init__(self, config_file_path) :
		config_file = open(config_file_path, 'r')
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

