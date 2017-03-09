# -*- coding: utf-8 -*-
"""
	tests.app
	---------------
	Test application

	:author: Prev(prevdev@gmail.com)
"""


import pytest
from jikji import Jikji


def test_app() :
	jikji = Jikji('sample')
	jikji.generate()

