# -*- coding: utf-8 -*-
"""
	jikji/utils
	----------------
	Utils of jikji
	History, Cache

	:author: Prev(prevdev@gmail.com)
"""

import os
import shutil
import json
import re
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



