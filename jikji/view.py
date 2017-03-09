# -*- coding: utf-8 -*-
"""
	jikji/view
	---------------
	View, Page Class

	:author: Prev(prevdev@gmail.com)
"""

import os
from datetime import datetime
from . import utils


def makeviews(rules) :
	for rule in rules :
		View.addview(*rule)


def view(viewid) :
	return View.getview(viewid)



class View() :
	_views = {}

	@staticmethod
	def getviews() :
		return list(View._views.values())

	@staticmethod
	def getview(viewid) :
		return View._views[viewid]

	@staticmethod
	def addview(viewid, url_rule, template_path, options=None) :
		View._views[viewid] = View(
			id = viewid,
			url_rule = url_rule,
			template_path = template_path,
			options = options
		)


	def __init__(self, id, url_rule, template_path, options=None) :
		self.id = id
		self.url_rule = url_rule
		self.template_path = template_path
		self.options = options
		self.pages = []


	def addpage(self, *params) :
		self.pages.append(Page(self, params))


	def init_viewmodel(self, settings) :
		tmp = self.id.split('.')

		path = os.path.join(*tmp[0:-1])
		path = os.path.join(settings.VIEWMODEL_ROOT, path + '.py')


		module = utils.load_module(path)
		function_name = tmp[-1]

		self.viewmodel = module.__dict__[ function_name ]
		return self.viewmodel


class Page :
	def __init__(self, view, params) :
		self.view = view
		self.params = params


	def getcontext(self) :
		context = self.view.viewmodel( *self.params )

		if type(context) == dict :
			# THINK: better way to provide page info?
			context['_page'] = {
				'url': self.geturl(),
				'template': self.view.template_path,
				'render_time': datetime.now(),
			}

		return context


	def geturl(self) :
		url = self.view.url_rule

		for index, param in enumerate(self.params) :
			url = url.replace('$%d' % (index+1), param)

		return url
