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
		
		historydir = config.sitepath + '/.jikji/history'
		os.makedirs(historydir, exist_ok=True )


		# Get history dir of now time
		now = datetime.now()
		nowstr = now.strftime('%y-%m-%d %H:%M:%S.%f')
		cur_historydir = '%s/%s' % (historydir, nowstr)


		if not os.path.isdir(cur_historydir) :
			os.mkdir(cur_historydir)

		self._config = config
		self.historydir = historydir
		self.cur_historydir = cur_historydir



	def log(self) :
		""" logh history
		"""
		
		# Log terminal.log
		terminal_capture = cprint.capture()

		with open('%s/terminal.log' % self.cur_historydir, 'w') as file:
			file.write(terminal_capture)


		# Copy output files to history
		shutil.copytree( self._config.path.output, '%s/%s' % (self.cur_historydir, 'output') )

