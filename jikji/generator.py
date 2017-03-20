"""
	jikji/generator
	----------------
	Static Page Generator
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil

from .cprint import cprint
from .view import View
from . import utils

class Generator :

	def __init__(self, app) :
		""" Constructor
		:param app: Jikji application instance
		"""

		self.app = app




	def generate(self) :
		""" Generate pages from views
		"""

		for view in self.app.getviews() :
			for page in view.pages :
				cprint.write(page.geturl() + ' ')

				self.create_output_file(
					content = page.getcontent(),
					url = page.geturl(),
					output_root = self.app.settings.OUTPUT_ROOT,
				)

				cprint.line('finish', green=True)
		

		self._copy_static_files(
			self.app.settings.STATIC_ROOT,
			self.app.settings.OUTPUT_ROOT,
		)



	def urltopath(self, url, output_dir) :
		""" Get full path of output
		"""
		if url[-1] == '/' : url += 'index.html'
		if url[0] == '/' : url = url[1:]
		
		return output_dir + '/' + url




	def create_output_file(self, content, url, output_root) :
		""" Create output file
		:params
			- content: content of file
			- url: url of page
			- output_root: root directory of output
		
		"""

		# if dictionary not exists, make dirs
		output_file = self.urltopath(url, output_root)
		os.makedirs( os.path.dirname(output_file), exist_ok=True )

		if type(content) == str :
			with open(output_file, 'w') as file:
				file.write(content)

		else :
			with open(output_file, 'wb') as file:
				file.write(content)
		


	def _copy_static_files(self, static_dir, output_root, dir=None) :
		""" Copy static files in <STATIC_PATH> declared in settings
		
		:params
			- static_dir: static dir to copy
			- output_root: output root dir that copied file will located to
			- dir: dir path for recursively explored (if value is None, use static_dir for first call)
		"""
		
		if dir is None : dir = static_dir
		if not os.path.isdir(dir) : return

		list = os.listdir(dir)
		
		for file in list :
			if file[0] == '.' :
				# continue if file is hidden
				continue

			filepath = os.path.join(dir, file)

			if os.path.isdir(filepath) :
				# if file is directory, call function recursively
				self._copy_static_files(static_dir, output_root, filepath)

			else :
				# filepath that common string of static_dir is removed
				trimed_path = filepath[ len(static_dir)+1 : ] 
				dst_path = os.path.join(output_root, trimed_path)

				os.makedirs( os.path.dirname(dst_path), exist_ok=True )
				shutil.copyfile(
					src = filepath,
					dst = dst_path
				)

				cprint.line('/%s [Asset]' % trimed_path)

