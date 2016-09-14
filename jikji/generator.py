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

from model import Model

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

		# read pages.xml
		with open(self.config.pages_xml_path(), 'r') as file:
			pages_config_content = file.read()

		# excute template by jinja
		tpl = jinja2.Template(pages_config_content)
		rendered_xml = tpl.render({
			'model': self.model
		})


		###################################
		# parse xml
		###################################

		tree = ET.fromstring(rendered_xml)
		page_tags = tree.findall('page')

		cnt = 0

		for page in page_tags :

			# open template file descripted in <template> tag
			with open(self.config.tpl_dir() + '/' + page.find('template').text, 'r') as file:
				tpl_content = file.read()
			
			tpl = jinja2.Template(tpl_content)

			# render with jinja template
			# Context is not parsed with json but ast
			#	because in pages xml, context value is not printed with json.dump
			output = tpl.render(
				ast.literal_eval(
					page.find('context').text
				)
			)

			# Get output's path
			url = page.find('url').text
			
			# If url is path, append index.html
			if url[-1] == '/' : url += 'index.html'

			# Get full path of output
			output_path = self.config.output_dir() + '/' + url

			# if dictionary not exists, make dirs
			os.makedirs( os.path.dirname(output_path), exist_ok=True )

			with open(output_path, 'w') as file:
				file.write(output)

			cnt += 1


		print('Generate completed\n%s pages are generated with jiki' % cnt)



	

	

