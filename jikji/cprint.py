# -*- coding: utf-8 -*-

"""
	jikji/cprint
	----------------
	print with color
	
	:author Prev(prevdev@gmail.com)
"""

import os


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def okb(msg) :
	print(bcolors.OKBLUE + msg + bcolors.ENDC)

def ok(msg) :
	print(bcolors.OKGREEN + msg + bcolors.ENDC)

def warn(msg) :
	print(bcolors.WARNING + msg + bcolors.ENDC)

def fail(msg) :
	print(bcolors.FAIL + msg + bcolors.ENDC)
	
def error(msg) :
	fail(msg)

def bold(msg) :
	print(bcolors.BOLD + msg + bcolors.ENDC)

def underline(msg) :
	print(bcolors.UNDERLINE + msg + bcolors.ENDC)


def line() :
	#rows, columns = os.popen('stty size', 'r').read().split()
	po = os.popen('stty size', 'r').read()
	
	if po :
		rows, columns = pp2.split()
		print('-' * (int(columns) - 1))