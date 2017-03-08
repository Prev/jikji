# -*- coding: utf-8 -*-
"""
	jikji/config
	---------------
	Config Manage Class

	:author: Prev(prevdev@gmail.com)
"""

import os

class Config :
	
	def __init__(self, sitepath) :
		
		self.sitepath = sitepath
		self.path = {
			'template' : os.path.join(sitepath, 'template'),
			'output' : os.path.join(sitepath, 'output'),
			'static': os.path.join(sitepath, 'static')
		}


