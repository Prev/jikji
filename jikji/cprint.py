# -*- coding: utf-8 -*-

"""
	jikji/cprint
	----------------
	print with color
	
	:author Prev(prevdev@gmail.com)
"""

from py.io import TerminalWriter

_tw = TerminalWriter()


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
	_tw.write(msg, **markup)

def line(msg='', **markup) :
	msg = str(msg)
	_tw.line(msg, **markup)

def sep(sep, title, **markup) :
	_tw.sep(sep, title, **markup)

def section(title=None, **markup) :
	_tw.sep('-', title, **markup)

