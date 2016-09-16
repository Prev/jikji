# -*- coding: utf-8 -*-
"""
	Jikji
	----------------
	Code-less static web generator based on RESTful API Server
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT
	
"""

if __name__ == '__main__' :
	import sys
	import os.path

	from .app import Jikji
	from . import cprint


	if len(sys.argv) < 2:
		cprint.error('usage: python3 -m jikji <config.json path>')
		sys.exit(-1)

	config_file = sys.argv[1]

	if os.path.isdir(config_file) :
		config_file += '/config.json'

	app = Jikji(config_file)
	app.generate()