# -*- coding: utf-8 -*-
"""
	tests.generator
	---------------
	Test generator of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest

import os
import shutil
from jikji import Jikji


def test_generate1() :
	""" Testing for generating of testapp1
	"""
	jikji = Jikji('tests/testapp1')
	OUTPUT_ROOT = jikji.settings.OUTPUT_ROOT

	if os.path.exists( OUTPUT_ROOT ) :
		shutil.rmtree( OUTPUT_ROOT )

	jikji.generate()

	for i in range(1, 5) :
		with open('%s/%s.html' % (jikji.settings.OUTPUT_ROOT, i), 'r') as f:
			c = f.read()
		assert c == '<div>%s</div>' % i




def test_generate2() :
	""" Testing for generating of testapp2
	"""
	jikji = Jikji('tests/testapp2')

	OUTPUT_ROOT = jikji.settings.OUTPUT_ROOT
	STATIC_ROOT = jikji.settings.STATIC_ROOT

	if os.path.exists( OUTPUT_ROOT ) :
		shutil.rmtree( OUTPUT_ROOT )

	jikji.generate()


	with open('%s/index.html' % OUTPUT_ROOT, 'r') as f : c = f.read()
	assert c == '<p>Hello</p><i>home.html</i>'


	with open('%s/README.md' % OUTPUT_ROOT, 'r') as f: c = f.read()
	with open('%s/README.md' % STATIC_ROOT, 'r') as f: c2 = f.read()
	assert c == c2


	with open('%s/requirements.txt' % OUTPUT_ROOT, 'r') as f :
		c = f.read()
	assert c == 'jikji>=2.0\nrequests>=2.11'



