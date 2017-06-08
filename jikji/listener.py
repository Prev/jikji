"""
	jikji/listener
	----------------
	Listening server for fast develop

	:author: Prev(prevdev@gmail.com)
"""

import os, shutil
import mimetypes
import flask
import jinja2

from . import utils
from .cprint import cprint

class Listener :

	def __init__(self, app) :
		""" Init Listener instance
		:param app: Jikji Application instance
		"""
		self.app = app
	
		# merge pages to one variable in each views
		npages = {}
		for pg in app.pagegroups :
			for page in pg.getpages() :
				url = self.format_url( page.geturl() )
				npages[url] = page

		self.pages = npages



	def listen(self, port, host) :
		""" Start listening HTTP server with Flask
		"""
		cprint.section('Listening %s pages' % len(self.pages))
		for index, url in enumerate(self.pages) :
			if index > 20 :
				cprint.line('...')
				break
			cprint.line('/' + url)

		cprint.section('Open Local Server with Flask (%d pages)' % len(self.pages))

		flaskapp = flask.Flask(__name__)
		flaskapp.add_url_rule('/', 'index', self.response)
		flaskapp.add_url_rule('/__pages', 'list_pages', self.list_pages)
		flaskapp.add_url_rule('/<path:url>', 'response', self.response)
		flaskapp.run(port=port, host=host)

		self.flaskapp = flaskapp



	def format_url(self, url) :
		""" Format url to check equals
		"""
		if len(url) >= 10 and url[-10:] == 'index.html' :
			url = url[:-10]

		if len(url) >= 1 and url[0] == '/' :
			url = url[1:]
		# if len(url) > 1 and url[-1] == '/' :
		# 	url = url[0:-1]

		return url


	def list_pages(self) :
		headers = {'Content-type': 'text/html'}
		body = '<h1>Listening Pages</h1><ul>'

		for pg in self.app.pagegroups :
			body += '<li>'

			for page in pg.getpages() :
				url = self.format_url( page.geturl() )
				body += '<a href="/%s">/%s</a><br>' % (url, url)

			body += '</li>'
	

		return body, 200, headers



	def response(self, url='') :
		""" Response content from url
			If url exists in pages, render template in realtime and return output
			Else, Find files in assets dir.
		"""
		url = self.format_url(url)
		type = mimetypes.guess_type(url)[0]

		headers = {}
		if type is not None :
			headers['Content-type'] = type


		if url in self.pages :
			page = self.pages[url]

			# Reload settings of generator
			self.app._load_settings_to_jinja_env()

			# Reload view file
			import inspect
			module = inspect.getmodule(page.view.viewfunc)
			utils.load_module(module.__file__, self.app.settings.ROOT_PATH)

			output = page.getcontent()
			return output, 200, headers



		# Check for static files
		asset_path = os.path.join(self.app.settings.STATIC_ROOT, url)
		
		if os.path.isfile(asset_path) :
			with open(asset_path, 'rb') as file :
				content = file.read()

			return content, 200, headers


		filename = os.path.basename(url)

		if len(filename) > 0 and '.' not in filename :
			return flask.redirect(url + '/', code=302)

		return '<h1 align="center">404 NOT FOUND</h1>', 404
		


