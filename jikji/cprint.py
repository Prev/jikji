# -*- coding: utf-8 -*-

"""
	jikji/cprint
	------------------------------
	Print with color
	Capture terminal log to file
	
	:author Prev(prevdev@gmail.com)
"""

from py.io import TerminalWriter, StdCaptureFD

class cprint() :

	# Default Terminal Writer on 'py.std.sys.stdout'
	_tw = TerminalWriter()


	# Log Writer
	_lw = None
	_logfile = None


	def writers() :
		""" Return writers that be written
		"""
		if cprint._lw is not None :
			return (cprint._tw, cprint._lw)
		else :
			return (cprint._tw, )


	@staticmethod
	def capture_file(logfile_path) :
		""" Logging terminal output to logfile
		"""
		cprint._logfile = open(logfile_path, 'w+')
		cprint._lw = TerminalWriter(file=cprint._logfile) # log writer


	@staticmethod
	def end_capture_file() :
		""" End logging terminal output to logfile
		"""
		if cprint._logfile is not None :
			cprint._logfile.close()
		cprint._lw = None


	@staticmethod
	def ok(msg) :
		cprint.line(msg, green=True)


	@staticmethod
	def okb(msg) :
		cprint.line(msg, blue=True)


	@staticmethod
	def warn(msg) :
		cprint.line(msg, yellow=True)


	@staticmethod
	def fail(msg) :
		cprint.line(msg, red=True)
	

	@staticmethod
	def error(msg) :
		cprint.fail(msg)


	@staticmethod
	def bold(msg) :
		cprint.line(msg, bold=True)


	@staticmethod
	def write(msg, **markup) :
		for w in cprint.writers() :
			w.write(msg, **markup)
		

	@staticmethod
	def line(msg='', **markup) :
		for w in cprint.writers() :
			w.line(str(msg), **markup)


	@staticmethod
	def sep(sep, title, **markup) :
		for w in cprint.writers() :
			w.sep(sep, title, **markup)
		

	@staticmethod
	def section(title=None, **markup) :
		cprint.sep('-', title, **markup)


	