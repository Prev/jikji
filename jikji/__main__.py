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
	from .app import Jikji

	if len(sys.argv) < 2:
		print('usage: python3 -m jikji <config.json path>')
		sys.exit(-1)

	app = Jikji(sys.argv[1])
	app.generate()