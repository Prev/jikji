"""
	jikji/generator
	----------------
	Static Page Generator

	Generated files are created in ROOTPATH/.output
	After Generation, Publisher upload contents to destination 
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil, traceback
from multiprocessing import Pool
from datetime import datetime

from .cprint import cprint
from .utils import copytree2, AppDataUtil, Cache


def mkfile(path, content) :
	""" Create output file
	:param path: filepath of destination
	:param content: content of file
	"""

	# if dictionary not exists, make dirs
	os.makedirs( os.path.dirname(path), exist_ok=True )

	filemode = (type(content) == str) and 'w' or 'wb'
	with open(path, filemode) as file:
		file.write(content)



def urltopath(url, basedir=None) :
	""" Get full path by url and basedir
	"""
	
	if url[-1] == '/' : url += 'index.html'
	if url[0] == '/' : url = url[1:]
	
	if basedir :
		return os.path.join(basedir, url)
	else :
		return url



def generate_work(pagegroup) :
	""" Function called by multiprocessing.Process
	:param pagegroup: PageGroup Object
	"""

	success_pages = []; errors = []; ignored_pages=[]
	generator = Generator.getinstance()

	pagegroup.before_rendered()

	for page in pagegroup.getpages() :
		url = page.geturl()
		try :
			content = page.getcontent()
			path = generator.get_tmp_filepath(url)
			mkfile(path=path, content=content)

			success_pages.append(url)

		except Exception as e :
			errors.append({
				'url': url,
				'trackback': traceback.format_exc(),
				'exception': e,
			})


	kwarg = len(errors) and {'red': True} or {'green': True}
	cprint.write(
		pagegroup.get_representative_url() + ' (%d/%d) \n' % (len(success_pages), len(success_pages) + len(errors)),
		**kwarg
	)

	if len(errors) and generator.app.settings.__dict__.get('ATOMIC_PAGEGROUP', False):
		# If setting has `ATOMIC_PAGEGROUP` option, only publish none-error PageGroups
		for url in success_pages :
			path = generator.get_tmp_filepath(url)
			os.remove(path)

		ignored_pages = success_pages[:]
		success_pages = []


	pagegroup.after_rendered(success_pages, errors, ignored_pages)

	for e in errors :
		# Display errors if exists
		cprint.section( e['url'], red=True )
		cprint.line( e['trackback'], yellow=True )

	return success_pages, errors, ignored_pages, pagegroup
		


class Generator(AppDataUtil) :

	instance = None
	SFMTC_KEY = '__sfmtimes' # Static File Modified Time Cache Key

	@staticmethod
	def getinstance() :
		return Generator.instance


	def __init__(self, app) :
		""" Constructor
		:param app: Jikji application instance
		"""

		AppDataUtil.__init__(self, app)

		self.app = app
		self.tmp_output_root = self.appdata_path('output')

		self.sf_mtimes = Cache(app).get(Generator.SFMTC_KEY, {})

		Generator.instance = self


	def get_tmp_filepath(self, url) :
		""" Get temporarily filepath by url
		"""
		return urltopath(url, self.tmp_output_root)


	def check_static_file_is_modified(self, trimed_path, fullpath) :
		""" Check whether static file is modified with Cache
		"""
		if self.sf_mtimes.get(trimed_path, -1) >= os.path.getmtime(fullpath) :
			# If static file's rendered time is ahead of files' modified time, ignore it
			self.generation_result[-1][2].append('/' + trimed_path) # Add to ignored_pages
			return False


	def set_static_file_created(self, trimed_path, fullpath) :
		""" Set static file is modified in Cache
		"""

		self.sf_mtimes[trimed_path] = datetime.now().timestamp()
		self.generation_result[-1][0].append('/' + trimed_path) # Add to success_pages

		cprint.line('/%s [Asset]' % trimed_path)



	def generate(self) :
		""" Generate pages from app
		"""

		if os.path.exists( self.tmp_output_root ) :
			shutil.rmtree( self.tmp_output_root )


		if 'sclear' in self.app.options :
			self.sf_mtimes = {}


		# Generate page with multiprocessing
		processes_cnt = self.app.settings.__dict__.get('PROCESSES', 4)

		pool = Pool(processes=processes_cnt)
		self.generation_result = pool.map(generate_work, self.app.pagegroups)
		

		# Copy static files to tmp-output dir
		self.generation_result.append(([], [], [], None))
		copytree2(
			src = self.app.settings.STATIC_ROOT,
			dst = self.tmp_output_root,
			callback_before = self.check_static_file_is_modified,
			callback_after = self.set_static_file_created,
		)

		Cache(self.app).set(Generator.SFMTC_KEY, self.sf_mtimes)

		return self.generation_result

	


