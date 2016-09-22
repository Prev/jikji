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

	def _check_log_enabled(self) :
		return self._config.log_history
		

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
		cur_historydir = '%s/%s' % (historydir, nowstr)


		if not os.path.isdir(cur_historydir) :
			os.mkdir(cur_historydir)

		self.historydir = historydir
		self.cur_historydir = cur_historydir



	def log(self) :
		""" log history
		"""

		if not self._check_log_enabled() : return
		
		# Log terminal.log
		terminal_capture = cprint.capture()

		with open('%s/terminal.log' % self.cur_historydir, 'w') as file:
			file.write(terminal_capture)


		# Copy output files to history
		try :
			shutil.copytree( self._config.path.output, '%s/%s' % (self.cur_historydir, 'output') )
		except FileExistsError:
			pass



