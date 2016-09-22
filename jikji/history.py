# -*- coding: utf-8 -*-
"""
	jikji/history
	----------------
	History manager

	:author: Prev(prevdev@gmail.com)
"""

import os
import shutil
from datetime import datetime

from . import cprint

class History :

	
	def __init__(self, config) :
		""" Init History Class with config
		"""

		self._config = config

		if not self._check_log_enabled() : return

		
		historydir = config.sitepath + '/.jikji/history'
		os.makedirs(historydir, exist_ok=True )


		# Get history dir of now time
		now = datetime.now()
		nowstr = now.strftime('%y-%m-%d %H:%M:%S.%f')
		cur_historydir = os.path.join(historydir, nowstr)


		if not os.path.isdir(cur_historydir) :
			os.mkdir(cur_historydir)

		self.historydir = historydir
		self.cur_historydir = cur_historydir



	def _check_log_enabled(self) :
		""" Return log_history is enabled
		"""
		return self._config.log_history



	def log(self, filename, content) :
		""" log file to cur_historydir
		"""
		if not self._check_log_enabled() : return

		with open(os.path.join(self.cur_historydir, filename), 'w') as file:
			file.write(content)


	def log_terminal(self) :
		""" log terminal output
		"""
		terminal_capture = cprint.capture()
		self.log('terminal.log', terminal_capture)



	def log_outputs(self) :
		""" log output files
		"""
		if not self._check_log_enabled() : return
		
		try :
			shutil.copytree( self._config.path.output, os.path.join(self.cur_historydir, 'output') )
		except FileExistsError:
			pass


	


