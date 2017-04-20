"""
	jikji/generator
	----------------
	Static Page Generator
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil, traceback
from multiprocessing import Pool

from .cprint import cprint
from .view import View, Page, PageGroup
from . import utils


def generate_pages(params) :
	""" Function called by multiprocessing.Process

	:param params: tuple set
		pagegroup: PageGroup Object
		generator: Generator Object
	"""
	
	pagegroup, output_root = params

	pagegroup.before_rendered()
	success_pages = []
	error_pages = []
	errors = []

	for page in pagegroup.getpages() :
		url = page.geturl()
		try :
			content = page.getcontent()

			Generator.create_output_file(
				content = content,
				url = url,
				output_root = output_root,
			)
		except Exception as e :
			errors.append({
				'pagegroup': pagegroup,
				'page': page,
				'url': url,
				'trackback': traceback.format_exc(),
			})
			error_pages.append(url)

		else :
			success_pages.append( url )



	if len(error_pages) :	ctx = {'red': True}
	else : 					ctx = {'green': True}

	cprint.write(
		pagegroup.get_printing_url() + ' (%d/%d) \n' % (len(success_pages), len(success_pages) + len(error_pages)),
		**ctx
	)

	for e in errors :
		cprint.section( e['url'], red=True )
		cprint.line( e['trackback'], yellow=True )


	pagegroup.after_rendered()
	return success_pages, error_pages



class Generator :

	@staticmethod
	def urltopath(url, output_dir) :
		""" Get full path of output
		"""
		if url[-1] == '/' : url += 'index.html'
		if url[0] == '/' : url = url[1:]
		
		return output_dir + '/' + url


	@staticmethod
	def create_output_file(content, url, output_root) :
		""" Create output file
		:params
			- content: content of file
			- url: url of page
			- output_root: root directory of output
		"""

		# if dictionary not exists, make dirs
		output_file = Generator.urltopath(url, output_root)
		os.makedirs( os.path.dirname(output_file), exist_ok=True )

		if type(content) == str :
			with open(output_file, 'w') as file:
				file.write(content)

		else :
			with open(output_file, 'wb') as file:
				file.write(content)
		


	def __init__(self, app) :
		""" Constructor
		:param app: Jikji application instance
		"""
		self.app = app


	def generate(self) :
		""" Generate pages from views
		"""
		processes_cnt = self.app.settings.__dict__.get('PROCESSES', 4)
		pool = Pool(processes=4)

		params = zip(self.app.pagegroups, [self.app.settings.OUTPUT_ROOT] * len(self.app.pagegroups))
		result = pool.map(generate_pages, params)
		
		self._copy_static_files(
			self.app.settings.STATIC_ROOT,
			self.app.settings.OUTPUT_ROOT,
		)

		
		success_cnt = 0; error_cnt = 0

		for sucesses, errors in result :
			success_cnt += len(sucesses)
			error_cnt += len(errors)
		
		return (success_cnt, error_cnt)



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


