# -*- coding: utf-8 -*-
"""
	tests.app
	---------------
	Test application

	:author: Prev(prevdev@gmail.com)
"""


import pytest
from jikji import Jikji


def test_app0() :
	jikji = Jikji('sample')


def test_app1() :
	""" Simple Application with one View
	"""
	jikji = Jikji('tests/testapp1')


def test_app2() :
	""" Complex Application using static files, model, globals
		URL is configured in urls.py
	"""
	jikji = Jikji('tests/testapp2')


def test_app3() :
	""" Application using PageGroup notation
	"""
	jikji = Jikji('tests/testapp3')
	