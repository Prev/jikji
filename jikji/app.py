# -*- coding: utf-8 -*-
"""
	jikji/app
	----------------
	Jikji class implements

	:author: Prev(prevdev@gmail.com)
"""

import os, sys
import time
import jinja2

from . import __version__
from . import utils
from .cprint import cprint
from .generator import Generator
from .view import View, Page


def addpage(view, params=[]) :
	""" Add page to app
	"""
	app = Jikji.getinstance()

	if type(view) == str :
		view = getview(view)

	app.pages.append(Page(
		view=view,
		params=params,
	))

def getview(viewid) :
	""" Get View in app by id
	"""
	app = Jikji.getinstance()
	return app.views[viewid]


class Jikji :

	instance = None

	__attrs__ = [
		'settings',
		'jinja_env',
		'views',
		'page',
		'generator',
	]

	@staticmethod
	def getinstance() :
		return Jikji.instance
		

	def __init__(self, sitepath) :
		""" Initialize Jikji Application
		"""

		# Assign self to single-ton instance
		Jikji.instance = self

		self.pages = []


		cprint.line('using jikji %s' % __version__)
		cprint.bold('Init jikji application "%s"\n' % os.path.abspath(sitepath))
	

		# Load settings file		
		self.settings = utils.load_module(os.path.join(sitepath, 'settings.py'))


		# Init jinja2 env
		self.jinja_env = jinja2.Environment(
			loader = jinja2.FileSystemLoader( self.settings.TEMPLATE_ROOT ),
			autoescape = True,
			trim_blocks = True,
			lstrip_blocks = True
		)
		self._load_settings_to_jinja_env()


		# Add application dir to sys path
		sys.path.append(self.settings.ROOT_PATH)


		# Load view files
		cprint.section('Load views and init scripts')
		self.views = {}
		self._load_module_recursive( self.settings.VIEW_ROOT )


		# Load init scripts
		for file in self.settings.INIT_SCRIPTS :
			utils.load_module(file, self.settings.ROOT_PATH)


		# Get Max size of view-info printed
		max_printing_size = 0
		for view in self.getviews() :
			max_printing_size = max(
				max_printing_size,
				len(view.id)
			)

		# Print views
		for view in self.getviews() :
			spaces = " " * (max_printing_size - len(view.id) + 1)
			cprint.write(view.id, green=True)
			cprint.line(" %s%s" % (spaces, view.url_rule))




	def _load_settings_to_jinja_env(self) :
		""" Assign functions in settings to jinja_function
		"""
		# Load filters if exists
		if hasattr(self.settings, 'FILTERS') :
			for name, cls in utils.load_module(self.settings.FILTERS).__dict__.items() :
				self.jinja_env.filters[name] = cls


		# Load globals if exists
		if hasattr(self.settings, 'GLOBALS') :
			for name, cls in utils.load_module(self.settings.GLOBALS).__dict__.items() :
				self.jinja_env.globals[name] = cls




	def _load_module_recursive(self, dir) :
		""" Load module in directory recursively
		"""	
		for filepath in os.listdir(dir) :
			fullpath = os.path.join(dir, filepath)

			if os.path.isdir(fullpath) :
				self._load_module_recursive(fullpath)

			elif os.path.splitext(filepath)[1] == '.py' :
				utils.load_module(fullpath, self.settings.ROOT_PATH)




	def getviews(self) :
		""" Get all views
		"""
		return list(self.views.values())



	def register_view(self, view_func, url_rule=None) :
		""" Register view to application
		"""

		viewid = View.parse_id(view_func, self.settings.VIEW_ROOT)
		
		if viewid not in self.views :
			# Add view if not exists
			v = View(
				id = viewid,
				view_func = view_func,
				url_rule = url_rule,
			)
			self.views[viewid] = v

		else :
			# Update view if exists
			v = self.views[viewid]
			v.view_func = view_func

			if url_rule is not None :
				v.url_rule = url_rule

		return v



	def generate(self) :
		""" Generate Application
		"""
		generator = Generator(self)

		cprint.section('Generate Pages in Views')
		gen_start_time = time.time()

		generator.generate()
		
		cost_time = round(time.time() - gen_start_time, 2)
		cprint.sep('=', 'Generate completed in %s seconds' % cost_time, blue=True, bold=True)


