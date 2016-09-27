# -*- coding: utf-8 -*-
"""
	jikji/history
	----------------
	History manager

	:author: Prev(prevdev@gmail.com)
"""

import os
import os.path as path
import shutil
from datetime import datetime

from .cprint import cprint

class History :

	
	def __init__(self, config) :
		""" Init History Class with config
		"""

		self._config = config

		if not self.log_enabled : return

		
		historydir = path.join(config.sitepath, '.jikji', 'history')
		os.makedirs(historydir, exist_ok=True )


		# Get history dir of now time
		now = datetime.now()
		nowstr = now.strftime('%y-%m-%d %H:%M:%S.%f')
		cur_historydir = path.join(historydir, nowstr)


		# Make history dir of now time
		if not path.isdir(cur_historydir) :
			os.mkdir(cur_historydir)


		# Capture terminal log to "<cur_historydir>/terminal.log"
		cprint.capture_file( path.join(cur_historydir, 'terminal.log') )


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

		with open(path.join(self.cur_historydir, filename), 'w') as file:
			file.write(content)



	def log_generated_files(self) :
		""" log generated output files
		"""
		if not self.log_enabled : return
		
		try :
			shutil.copytree( self._config.path.output, path.join(self.cur_historydir, 'output') )
		except FileExistsError:
			pass


	def close(self) :
		""" Close opened files
		"""
		cprint.end_capture_file()


