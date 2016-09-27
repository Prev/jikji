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
import sys
import time
import jinja2
import xml.etree.ElementTree as ET
import traceback
import shutil

from .cprint import cprint
from .history import History
from .model import ModelException


class Generator :
	
	__attrs__ =[
		'config', 'configpath', 'model', 'history'
		'_gen_start_time'
	]


	def __init__(self, config, model) :
		""" Constructor
		:param configpath: jikji.config.Config instance
		:param model: jikji.model.Model instance
		"""

		self.config = config
		self.configpath = config.path
		self.model = model


	def generate(self) :
		""" Generate pages
		Read pages.xml, render with jinja2, parse rendered file, and create static web pages.
		"""

		self.history = History(self.config)
		self._gen_start_time = time.time()


		cprint.bold('Start generating "%s"\n' % os.path.abspath(self.configpath.sitepath))

		cprint.section('Parse pages.xml with Rest Server')
		cprint.bold('With Rest server "%s"\n' % self.model.get_baseurl())


		# render pages.xml
		try :
			rendered_data = self._render_pages_xml( self.configpath.pages_xml )
		
		except ModelException as e:
			self._finish(False, 'Model Error', e)

		except jinja2.exceptions.TemplateError as e :
			self._finish(False, 'Template Error occurs in pages.xml', e)



		# parse rendered pages.xml via xml.etree.ElementTree
		page_tags = ET.fromstring(rendered_data).findall('page')

		output_dir = self.configpath.output


		cprint.line()
		cprint.section('Rendering %d pages' % len(page_tags))
		cprint.bold('Output in "%s"\n' % output_dir)


		# template renderer Environment
		env = jinja2.Environment(
			loader=jinja2.FileSystemLoader( self.configpath.tpl )
		)
		

		for page in page_tags :
			template = env.get_template( page.find('template').text.strip() )

			path = self._get_output_file_path(
				url = page.find('url').text.strip(),
				output_dir = output_dir
			)

			# remove common string of output_dir in path
			trimed_path = path[ len(output_dir) : ]

			try :
				# Context is not parsed with json but ast
				#  because in pages xml, context value is not printed with json.dumps
				self._generate_page(
					output_file = path,
					context = ast.literal_eval( page.find('context').text.strip() ),
					template = template,
				)
			
			except jinja2.exceptions.TemplateError as e :
				cprint.error('%s' % trimed_path )
				self._finish(False, 'Template Error', e)


			cprint.ok('%s' % trimed_path )


		for asset_dir in self.configpath.assets :
			self._copy_asset_files(
				asset_dir = asset_dir,
				output_dir = output_dir
			)


		self._finish(True)



	def _finish(self, is_success, err_cause=None, err_instance=None) :
		""" Called when generation is finished
			If some error occurs, stop generation and exit program
		
		:param is_success: boolean
		:param err_cause: If `is_success` is false, print cause of error
		:param err_instance: jinja2.exceptions.<SomeError> or ModelException
		"""

		if is_success :
			cprint.section('Generate completed in %s seconds' % round(time.time() - self._gen_start_time, 2), **{'blue':True})
			
			self.history.log_generated_files()
			self.history.close()

		else :
			cprint.section()
			
			if type(err_instance) == jinja2.exceptions.TemplateSyntaxError :
				# Print template syntax error line and content of that line
				cprint.error( 'jinja2.exceptions.TemplateSyntaxError: ' + err_instance.message )
				cprint.line( '\nIn line %d:' % err_instance.lineno )
				cprint.line( err_instance.source.splitlines()[ err_instance.lineno - 1 ].strip() )
				cprint.line()

			else :
				traceback.print_exc()

			cprint.section('Generation Stopped by ' + err_cause , **{'red':True})
			self.history.close()

			sys.exit(-1)

		

	def _render_pages_xml(self, pages_xml_path) :
		""" Render pages.xml via jinja

		:param pages_xml_path: string
		:return string
		"""
		with open(pages_xml_path, 'r') as file:
			pages_config_content = file.read()


		tpl = jinja2.Template(pages_config_content)
		rendered_xml = tpl.render({
			'model': self.model,
			'time': time
		})

		self.history.log('pages.xml', rendered_xml)

		return rendered_xml


	def _get_output_file_path(self, url, output_dir) :
		""" Get full path of output
		"""
		if url[-1] == '/' : url += 'index.html'
		if url[0] == '/' : url = url[1:]
		
		return output_dir + '/' + url



	def _generate_page(self, output_file, context, template) :
		""" Generate page via page_obj)

		:params
			- output_file: output_file_path(url + output_dir) (string)
			- context: context dict of template (string)
			- template: jinja2 template instance
		
		"""


		# render with jinja template
		output = template.render(context)

		# if dictionary not exists, make dirs
		os.makedirs( os.path.dirname(output_file), exist_ok=True )

		with open(output_file, 'w') as file:
			file.write(output)


	
	def _copy_asset_files(self, asset_dir, output_dir, dir=None) :
		""" Copy asset files in <asset_dir> declared in config.json
		
		:params
			- asset_dir: asset dir to copy
			- output_dir: output dir that copied file will located to
			- dir: dir path for recursively explored (if value is None, use asset_dir for first call)
		"""
		
		if dir is None : dir = asset_dir


		list = os.listdir(dir)
		
		for file in list :
			if file[0] == '.' :
				# continue if file is hidden
				continue

			filepath = os.path.join(dir, file)

			if os.path.isdir(filepath) :
				# if file is directory, call function recursively
				self._copy_asset_files(asset_dir, output_dir, filepath)

			else :
				# filepath that common string of asset_dir is removed
				trimed_path = filepath[ len(asset_dir)+1 : ] 
				dst_path = os.path.join(output_dir, trimed_path)

				os.makedirs( os.path.dirname(dst_path), exist_ok=True )
				shutil.copyfile(
					src = filepath,
					dst = dst_path
				)

				cprint.line('/%s [Asset]' % trimed_path)


