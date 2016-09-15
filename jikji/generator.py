#-*- coding: utf-8 -*-

"""
Jikji/Generator
@author Prev(prevdev@gmail.com)


Static page Generator

First, read pages.xml and render this file via jinja2.
while rendering pages.xml, context data will downloaded in rest-server.

Next, parse rendered pages.xml and create static web pages.

"""

import ast
import os
import jinja2
import xml.etree.ElementTree as ET

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
		rendered_data = self._render_pages_xml( self.config.pages_xml_path() )

		tree = ET.fromstring(rendered_data)
		page_tags = tree.findall('page')

		cnt = 0

		for page in page_tags :
			with open(self.config.tpl_dir() + '/' + page.find('template').text, 'r') as file:
				tpl_content = file.read()


			# Context is not parsed with json but ast
			#	because in pages xml, context value is not printed with json.dump
			self._generate_page(
				url = page.find('url').text,
				context = ast.literal_eval( page.find('context').text ),
				template_content = tpl_content,
				output_dir = self.config.output_dir()
			)


			cnt += 1

		print('Generate completed\n%s pages are generated with jikji' % cnt)




	"""
	Render pages.xml via jinja
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
	@param url: url of page (string)
	@param context: context dict of template (string)
	@param template_content: string
	@param output_dir: string
	"""
	def _generate_page(self, url, context, template_content, output_dir) :
		tpl = jinja2.Template(template_content)
		output = tpl.render(context)

		if url[-1] == '/' : url += 'index.html'

		# Get full path of output
		output_path = output_dir + '/' + url

		# if dictionary not exists, make dirs
		os.makedirs( os.path.dirname(output_path), exist_ok=True )

		with open(output_path, 'w') as file:
			file.write(output)


	

	

