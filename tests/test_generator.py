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
	jikji = Jikji('tests/test_site/config1.json')
	output_dir = jikji.config.path.output
	assets_dir = jikji.config.path.assets[0]

	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )

	jikji.generate()



	for i in range(1, 5) :
		with open('%s/%s.html' % (output_dir, i), 'r') as f: c = f.read()
		assert c == '<div>%s</div>' % i


	with open('%s/index.html' % output_dir, 'r') as f : c = f.read()
	assert c == '<p>Hello</p>'


	with open('%s/README.md' % output_dir, 'r') as f: c = f.read()
	with open('%s/README.md' % assets_dir, 'r') as f: c2 = f.read()
	assert c == c2




def test_generate2() :
	jikji = Jikji('tests/test_site/config2.json')
	output_dir = jikji.config.path.output

	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )

	jikji.generate()



