# -*- coding: utf-8 -*-
"""
	jikji/listener
	----------------
	Listening server for fast develop

	:author: Prev(prevdev@gmail.com)
"""

import os
import mimetypes

import flask
import jinja2

class Listener :

	def __init__(self, app, pages) :
		""" Init Listener instance
		:param app: Jikji app istance
		:param pages: array of page info returned from generator:render_pages_xml
		"""
		self.app = app
		

		# change data format for pages
		# array to dict which key is url
		npages = {}
		for page in pages :
			url = self.format_url( page['url'] )
			npages[url] = ( page['template'], page['context'] )

			print('/' + url)

		self.pages = npages



	def listen(self, port, host) :
		""" Start listening HTTP server with Flask
		"""
		flaskapp = flask.Flask(__name__)

		flaskapp.add_url_rule('/', 'index', self.response)
		flaskapp.add_url_rule('/<path:url>', 'response', self.response)
		flaskapp.run(port=port, host=host)


	def format_url(self, url) :
		""" Format url to check equals
		"""
		if len(url) >= 10 and url[-10:] == 'index.html' :
			url = url[:-10]

		if len(url) >= 1 and url[0] == '/' :
			url = url[1:]
		if len(url) > 1 and url[-1] == '/' :
			url = url[0:-1]

		return url


	def response(self, url='') :
		""" Response content from url
			If url exists in pages.xml data, render template in realtime and return output
			Else, Find files in assets dir.
		"""
		url = self.format_url(url)

		if url in self.pages :
			tpl = self.pages[url][0]
			context = self.pages[url][1]

			# Render template with jinja
			env = jinja2.Environment( loader=jinja2.FileSystemLoader( self.app.config.path.tpl ) )
			template = env.get_template(tpl)

			output = template.render(context)
			return output


		for assetdir in self.app.config.path.assets :
			# Return asset if exists
			path = os.path.join(assetdir, url)

			if os.path.isfile(path) :
				with open(path, 'rb') as file :
					content = file.read()

				type = mimetypes.guess_type(url)[0]
				return content, 200, {'Content-type': type}


		return '<h1 align="center">404 NOT FOUND</h1>', 404
		


