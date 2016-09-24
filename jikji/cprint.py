# -*- coding: utf-8 -*-

"""
	jikji/cprint
	----------------
	print with color
	
	:author Prev(prevdev@gmail.com)
"""

from py.io import TerminalWriter, StdCaptureFD

# logging terminal output to temp file
_log_file = open('.jikji.terminal.log', 'w+')


_tw = TerminalWriter()
_lw = TerminalWriter(file=_log_file) # log writer


def ok(msg) :
	line(msg, **{'green': True})

def okb(msg) :
	line(msg, **{'blue': True})

def warn(msg) :
	line(msg, **{'yellow': True})

def fail(msg) :
	line(msg, **{'red': True})
	
def error(msg) :
	fail(msg)

def bold(msg) :
	line(msg, **{'bold': True})


def write(msg, **markup) :
	for w in (_tw, _lw) :
		w.write(msg, **markup)
	

def line(msg='', **markup) :
	for w in (_tw, _lw) :
		w.line(str(msg), **markup)

def sep(sep, title, **markup) :
	for w in (_tw, _lw) :
		w.sep(sep, title, **markup)
	

def section(title=None, **markup) :
	sep('-', title, **markup)



def capture() :
	""" Read logging temp file and reset it
	:return: terminal printed string
	"""
	global _log_file

	_log_file.seek(0)
	out = _log_file.read()

	_log_file.truncate()
	return out
