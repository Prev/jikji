"""
	jikji/generator
	----------------
	Static Page Renderer
	
	:author Prev(prevdev@gmail.com)
"""

import os
import jinja2

from .cprint import cprint
from .view import View

class Generator :

	def __init__(self, config) :
		""" Constructor
		:param config: jikji.config.Config instance
		:param model: jikji.model.Model instance
		"""

		self.config = config

		# Init jinja2 env
		self.jinja_env = jinja2.Environment(
			loader = jinja2.FileSystemLoader( self.config.path['template'] ),
			autoescape = True,
			trim_blocks = True,
			lstrip_blocks = True
		)
	

	def generate(self) :
		""" Generate pages from views
		"""

		for view in View.getviews() :

			for page in view.pages :
				cprint.write(page.geturl() + ' ')

				output = self.generate_page(
					template_path = view.template_path,
					context = page.getcontext(),
					output_file = self.urltopath(page.geturl(), self.config.path['output'])
				)

				cprint.line('finish', green=True)
	


	def urltopath(self, url, output_dir) :
		""" Get full path of output
		"""
		if url[-1] == '/' : url += 'index.html'
		if url[0] == '/' : url = url[1:]
		
		return output_dir + '/' + url



	def generate_page(self, template_path, context=None, output_file=None, content=None) :
		""" Generate page

		:params
			- template_path: template file path
			- context: context dict of template (string)
			- output_file: output_file_path(url + output_dir) (string)
				if None, do not make file (default)
			- content: content of file (if context is None, using this)
		
		"""

		# render with jinja template
		if template_path is None and content is not None:
			output = content
		else :
			jtpl = self.jinja_env.get_template(template_path)
			output = jtpl.render( context )


		if output_file is not None :
			# if dictionary not exists, make dirs
			os.makedirs( os.path.dirname(output_file), exist_ok=True )

			with open(output_file, 'w') as file:
				file.write(output)

		return output

