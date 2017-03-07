# -*- coding: utf-8 -*-
"""
	jikji/app
	----------------
	Jikji class implements

	:author: Prev(prevdev@gmail.com)
"""

import os
import time
from . import __version__
from . import utils
from .cprint import cprint
from .generator import Generator
from .view import View
from .config import Config

class Jikji :

	def __init__(self, sitepath) :
		self.sitepath = sitepath
		self.config = Config(sitepath)
		self.generator = Generator(self.config)


		cprint.line('using jikji %s' % __version__)
		cprint.bold('Start generating "%s"\n' % os.path.abspath(self.config.sitepath))
		cprint.section('Load Views from pages.py')

		m = utils.load_module('pages', sitepath)

		for view in View.getviews() :
			#cprint.line("%s\t[%d pages]\t%s" % (view.id, len(view.pages), view.url_rule))

			cprint.write(view.id, green=True)
			cprint.line("\t[%d pages]\t%s" % (len(view.pages), view.url_rule))
			view.find_callee(sitepath)

		cprint.line('')



	def generate(self) :
		cprint.section('Generate Pages in Views')
		gen_start_time = time.time()

		self.generator.generate()
		
		cost_time = round(time.time() - gen_start_time, 2)
		cprint.sep('=', 'Generate completed in %s seconds' % cost_time, blue=True, bold=True)


