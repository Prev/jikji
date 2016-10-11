# -*- coding: utf-8 -*-
"""
	jikji/utils
	----------------
	Utils of jikji
	History, Cache

	:author: Prev(prevdev@gmail.com)
"""

import os, shutil, sys
import json
import re
import importlib
from datetime import datetime
from urllib.parse import quote_plus, unquote_plus

from .cprint import cprint


class AppDataUtil :
	def __init__(self, sitepath) :
		self.datapath = os.path.join(sitepath, '.jikji')



class Cache(AppDataUtil) :

	def __init__(self, sitepath) :
		""" Init Cache Class with sitepath
		"""

		AppDataUtil.__init__(self, sitepath)
		
		self.cachedir = os.path.join(self.datapath, 'cache')
		os.makedirs(self.cachedir, exist_ok=True )


	def getpath(self, key) :
		""" Get cache file path of key
		"""
		return os.path.join(self.cachedir, quote_plus(key))


	def get(self, key, default=None) :
		""" Get cached data with key
		If cache not found, return default value of param (default: None)
		"""
		cpath = self.getpath(key)
		
		if os.path.isfile(cpath) :
			with open(cpath, 'r') as file:
				content = file.read()

			return json.loads(content)

		else :
			return default


	def set(self, key, value) :
		""" Set cache data with key, value
		"""
		cpath = self.getpath(key)

		with open(cpath, 'w') as file:
			file.write( json.dumps(value) )


	def list(self, details=False) :
		""" Listing cache files
		"""
		clist = os.listdir(self.cachedir)

		if details :
			nlist = []

			for file in clist :
				filepath = os.path.join(self.cachedir, file)
				nlist.append('%s (%s bytes)' % (unquote_plus(file), os.path.getsize(filepath) ) )

			return nlist

		else :
			return clist


	def remove(self, key, as_pattern=False) :
		""" Remove cache data

		:param key: Key for cache or pattern if as_pattern is True
		:param as_pattern: Remove caches that matches with 'key' as regex
		"""

		if not as_pattern :
			cpath = self.getpath(key)

			if os.path.isfile(cpath) :
				os.remove(cpath)
				cprint.line('Cache "%s" is removed' % cpath)
			else :
				cprint.error('Cache "%s" not exists' % cpath)


		else :
			r = re.compile(key)
			clist = self.list()

			something_removed = False

			for file in clist :
				filepath = os.path.join(self.cachedir, file)

				if r.match(filepath) is not None :
					os.remove(filepath)

					something_removed = True
					cprint.line('Removed: %s' % filepath)

			if not something_removed :
				cprint.warn('No pattern matched file with "%s"' % key)


	def remove_all(self) :
		""" Remove all cache data
		"""
		self.remove('.*', as_pattern=True)




class History(AppDataUtil) :

	def __init__(self, config) :
		""" Init History Class with config
		"""

		AppDataUtil.__init__(self, config.sitepath)

		self._config = config
		if not self.log_enabled : return

		
		historydir = os.path.join(self.datapath, 'history')
		os.makedirs(historydir, exist_ok=True )


		# Get history dir of now time
		now = datetime.now()
		nowstr = now.strftime('%y-%m-%d %H:%M:%S.%f')
		cur_historydir = os.path.join(historydir, nowstr)


		# Make history dir of now time
		if not os.path.isdir(cur_historydir) :
			os.mkdir(cur_historydir)


		# Capture terminal log to "<cur_historydir>/terminal.log"
		cprint.capture_file( os.path.join(cur_historydir, 'terminal.log') )


		self.historydir = historydir
		self.cur_historydir = cur_historydir


	@property
	def log_enabled(self) :
		""" Return log_history is enabled
		"""
		return self._config.log_history



	def log(self, filename, content) :
		""" log file to cur_historydir
		"""
		if not self.log_enabled : return

		with open(os.path.join(self.cur_historydir, filename), 'w') as file:
			file.write(content)



	def log_generated_files(self) :
		""" log generated output files
		"""
		if not self.log_enabled : return
		
		try :
			shutil.copytree( self._config.path.output, os.path.join(self.cur_historydir, 'output') )
		except FileExistsError:
			pass


	def close(self) :
		""" Close opened files
		"""
		cprint.end_capture_file()



class ImportTool() :

	@staticmethod
	def assign(target, modules, sitepath='') :
		""" Import modules to target
		:params
			- target: target to assign module (dictionary)
			- modules: list of importing module
				- if value is string, import module by string
				- if value is list, import module by first element([0]) and get attr of module by second element([1])
			- sitepath: path of rendering site. Load module if file is exists in sitepath
		"""

		for module_name in modules :
			if isinstance(module_name, list) :
				module, _ = ImportTool.import_module(module_name[0], sitepath)

				attr_name = module_name[1]
				target[attr_name] = getattr(module, attr_name)

			else :
				module, module_name = ImportTool.import_module(module_name, sitepath)
				target[module_name] = module



	@staticmethod
	def import_module(module_name, path='') :
		""" Import module
			If module exists in python lib, load by importlib
			Else, find module by path
		"""
		module = None

		try :
			# Load module by importlib
			module = importlib.import_module(module_name)

		except ImportError as e:
			if module_name.find('/') != -1 :
				# if module name is path, process it
				tmp = module_name.split('/')
				module_name = tmp.pop()
				path = os.path.join( path, *tmp )


			if path != '' and path[-3:] != '.py' :
				# Make directory path to file path by joining
				path = os.path.join(path, module_name + '.py')

			if sys.version_info >= (3, 5) :
				# For python 3.5+
				spec = importlib.util.spec_from_file_location(module_name, path)
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(lib)
				

			else :
				# For python 3.3 and 3.4
				from importlib.machinery import SourceFileLoader
				module = SourceFileLoader(module_name, path).load_module()


			if module is None :
				raise e

		return module, module_name






