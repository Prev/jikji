"""
	jikji/generator
	----------------
	Static Page Generator
	
	:author Prev(prevdev@gmail.com)
"""

import os, shutil, traceback
from multiprocessing import Pool

from .cprint import cprint
from . import utils, publisher


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



def urltopath(url, basedir) :
	""" Get full path by url and basedir
	"""
	
	if url[-1] == '/' : url += 'index.html'
	if url[0] == '/' : url = url[1:]
		
	return os.path.join(basedir, url)



def generate_work(pagegroup) :
	""" Function called by multiprocessing.Process
	:param pagegroup: PageGroup Object
	"""

	success_pages = []; errors = []
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
				'pagegroup': pagegroup,
				'page': page,
				'url': url,
				'trackback': traceback.format_exc(),
				'exception': e,
			})


	kwarg = len(errors) and {'red': True} or {'green': True}
	cprint.write(
		pagegroup.get_printing_url() + ' (%d/%d) \n' % (len(success_pages), len(success_pages) + len(errors)),
		**kwarg
	)

	if len(errors) and generator.app.settings.__dict__.get('ATOMIC_PAGEGROUP', False):
		# If setting has `ATOMIC_PAGEGROUP` option, only publish none-error PageGroups
		for p in success_pages :
			os.remove(p)


	pagegroup.after_rendered(success_pages, errors)

	for e in errors :
		# Display errors if exists
		cprint.section( e['url'], red=True )
		cprint.line( e['trackback'], yellow=True )

	return success_pages, errors
		


class Generator :

	instance = None

	@staticmethod
	def getinstance() :
		return Generator.instance


	def __init__(self, app) :
		""" Constructor
		:param app: Jikji application instance
		"""
		self.app = app
		self.tmp_output_root = os.path.join(self.app.settings.ROOT_PATH, '.output')
		
		Generator.instance = self


	def get_tmp_filepath(self, url) :
		""" Get temporarily filepath by url
		"""
		return urltopath(url, self.tmp_output_root)



	def generate(self) :
		""" Generate pages from app
		"""

		if os.path.exists( self.tmp_output_root ) :
			shutil.rmtree( self.tmp_output_root )

		# Generate page with multiprocessing
		processes_cnt = self.app.settings.__dict__.get('PROCESSES', 4)
		pool = Pool(processes=4)
		result = pool.map(generate_work, self.app.pagegroups)
		

		# Copy static files to tmp output dir
		utils.copytree2(
			src = self.app.settings.STATIC_ROOT,
			dst = self.tmp_output_root,
			callback_after = lambda x, y : cprint.line('/%s [Asset]' % x),
		)


		# Publish
		pub = publisher.LocalPublisher(generator=self)
		pub.publish()
		

		success_cnt = 0; error_cnt = 0
		for sucesses, errors in result :
			success_cnt += len(sucesses)
			error_cnt += len(errors)
		
		return (success_cnt, error_cnt)



	


