# -*- coding: utf-8 -*-
"""
	jikji/generator
	----------------
	Static page Generator

	First, read pages.xml and render this file via jinja2.
	while rendering pages.xml, context data will downloaded in rest-server.

	Next, parse rendered pages.xml and create static web pages.

	
	:author Prev(prevdev@gmail.com)
"""

import ast
import os
import time
import jinja2
import xml.etree.ElementTree as ET
from . import cprint

class Generator :
	
	"""
	Constructor
	@param config: jikji.config.Config instance
	"""
	def __init__(self, config, model) :
		self.config = config
		self.model = model



	"""
	Generate pages
	Read pages.xml, render with jinja2, parse rendered file, and create static web pages.
	"""
	def generate(self) :
		start_time = time.time()


		cprint.bold('Start generating "%s"' % self.config.site_path)

		cprint.section('Parse pages.xml with Rest Server')
		cprint.bold('With Rest server "%s"\n' % self.config.rest_server_info()['base_url'])


		# render pages.xml
		rendered_data = self._render_pages_xml( self.config.pages_xml_path() )
		
		# parse rendered pages.xml via xml.etree.ElementTree
		page_tags = ET.fromstring(rendered_data).findall('page')

		output_dir = self.config.output_dir()


		cprint.line()
		cprint.section('Rendering %d pages' % len(page_tags))
		cprint.bold('Output in "%s"\n' % output_dir)


		# template renderer Environment
		env = jinja2.Environment(
			loader=jinja2.FileSystemLoader( self.config.tpl_dir() )
		)
		
		for page in page_tags :
			template = env.get_template( page.find('template').text )

			# Context is not parsed with json but ast
			#  because in pages xml, context value is not printed with json.dump
			path = self._generate_page(
				url = page.find('url').text,
				context = ast.literal_eval( page.find('context').text.strip() ),
				template = template,
				output_dir = output_dir
			)

			cprint.ok('%s' % path[len(output_dir):] )


		# cprint.line()
		cprint.section('Generate completed in %s seconds' % round(time.time() - start_time, 2), **{'blue':True})




	"""
	Render pages.xml via jinja
	@param pages_xml_path: string
	@return string
	"""
	def _render_pages_xml(self, pages_xml_path) :
		with open(pages_xml_path, 'r') as file:
			pages_config_content = file.read()


		tpl = jinja2.Template(pages_config_content)
		rendered_xml = tpl.render({
			'model': self.model
		})

		return rendered_xml



	"""
	Generate page via page_obj)
	@params
		- url: url of page (string)
		- context: context dict of template (string)
		- template: jinja2 template instance
		- output_dir: string
	
	@return output_path(string)
	"""
	def _generate_page(self, url, context, template, output_dir) :
		if url[-1] == '/' : url += 'index.html'
		if url[0] == '/' : url = url[1:]

		# render with jinja template
		output = template.render(context)

		# Get full path of output
		output_path = output_dir + '/' + url

		# if dictionary not exists, make dirs
		os.makedirs( os.path.dirname(output_path), exist_ok=True )

		with open(output_path, 'w') as file:
			file.write(output)

		return output_path


	

	

