#-*- coding: utf-8 -*-

if __name__ == '__main__' :
	import sys
	from .app import Jikji

	if len(sys.argv) < 2:
		print('usage: python3 -m jikji <config.json path>')
		sys.exit(-1)

	app = Jikji(sys.argv[1])
	app.generate()