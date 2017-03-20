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
	jikji = Jikji('tests/testapp1')


def test_app2() :
	jikji = Jikji('tests/testapp2')
	