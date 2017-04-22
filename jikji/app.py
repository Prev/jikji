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
from .view import View, Page, PageGroup
from .generator import Generator


def addpage(page=None, view=None, params=[]) :
	""" Add page to app
	"""

	if not page :
		page = Page(
			view=view,
			params=params,
		)

	Jikji.getinstance().pagegroups.append(
		PageGroup(page=page)
	)
	return page


def addpagegroup(pagegroup) :
	""" Add PageGroup to app
	"""
	Jikji.getinstance().pagegroups.append(pagegroup)


def getview(viewid) :
	""" Get View in app by id
	"""
	return Jikji.getinstance().getview(viewid)



class Jikji :

	instance = None

	__attrs__ = [
		'settings',
		'jinja_env',
		'views',
		'pagegroups',
		'generator',
	]

	@staticmethod
	def getinstance() :
		""" Get current Jikji app instance (single-ton)
		"""
		return Jikji.instance
		

	def __init__(self, sitepath) :
		""" Initialize Jikji Application
		"""

		# Assign self to single-ton instance
		Jikji.instance = self

		self.pagegroups = []


		cprint.line('using jikji %s' % __version__)
		cprint.bold('Init jikji application "%s"\n' % os.path.abspath(sitepath))
		
		# Add application dir to sys path
		sys.path.append(sitepath)

		# Load settings file		
		self.settings = utils.load_module(os.path.join(sitepath, 'settings.py'))


		if sitepath != self.settings.ROOT_PATH :
			sys.path.append(self.settings.ROOT_PATH)


		# Init jinja2 env
		self.jinja_env = jinja2.Environment(
			loader = jinja2.FileSystemLoader( self.settings.TEMPLATE_ROOT ),
			autoescape = True,
			trim_blocks = True,
			lstrip_blocks = True
		)
		self._load_settings_to_jinja_env()


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




	def getviews(self) :
		""" Get all views
		"""
		return list(self.views.values())



	def getview(self, viewid=None, viewfunc=None) :
		""" Get View by viewid or viewfunc
		"""
		if not viewid and not viewfunc :
			raise Exception('You must specify either viewid or viewfunc')

		if viewfunc :
			viewid = View.parse_id(viewfunc, self.settings.VIEW_ROOT)


		if viewid in self.views :
			return self.views[viewid]
		else :
			raise Exception('View "%s" not exists in app' % viewid)



	def register_view(self, viewfunc, url_rule=None) :
		""" Register view to application

			:param viewfunc: View function (callee of page)
			:param url_rule: URL Rule of View (You can change URL Rule with `getview` function)
		"""

		viewid = View.parse_id(viewfunc, self.settings.VIEW_ROOT)
		
		if viewid not in self.views :
			# Add view if not exists
			v = View(
				id = viewid,
				viewfunc = viewfunc,
				url_rule = url_rule,
			)
			self.views[viewid] = v

		else :
			# Update view if exists
			v = self.views[viewid]
			v.viewfunc = viewfunc

			if url_rule is not None :
				v.url_rule = url_rule

		return v



	def generate(self) :
		""" Generate Application
		"""
		generator = Generator(self)

		cprint.section('Generate Pages')
		gen_start_time = time.time()

		sucess_cnt, err_cnt = generator.generate()
		cost_time = round(time.time() - gen_start_time, 2)
		cprint.sep('=', 'Generate completed in %s seconds (%d success %d errors)' % (cost_time, sucess_cnt, err_cnt), blue=True, bold=True)




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
