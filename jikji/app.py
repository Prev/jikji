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

class Jikji :

	def __init__(self, sitepath) :

		cprint.line('using jikji %s' % __version__)
		cprint.bold('Init jikji application "%s"\n' % os.path.abspath(sitepath))
	

		# Load settings file		
		self.settings = utils.load_module(os.path.join(sitepath, 'settings.py'))


		# Load pages config file
		cprint.section('Load Views from pages.py')
		utils.load_module(self.settings.PAGES)


		# Init views
		for view in View.getviews() :
			cprint.write(view.id, green=True)
			cprint.line("\t[%d pages]\t%s" % (len(view.pages), view.url_rule))

			view.init_viewmodel(self.settings)


		cprint.line('')

		# Init generator
		self.generator = Generator(self.settings)



	def generate(self) :
		cprint.section('Generate Pages in Views')
		gen_start_time = time.time()

		self.generator.generate()
		
		cost_time = round(time.time() - gen_start_time, 2)
		cprint.sep('=', 'Generate completed in %s seconds' % cost_time, blue=True, bold=True)


