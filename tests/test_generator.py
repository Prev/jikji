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

	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )

	jikji.generate()

	for i in range(1, 5) :
		with open('%s/%s.html' % (output_dir, i), 'r') as f: c = f.read()
		assert c == '<div>%s</div>' % i


def test_generate2() :
	jikji = Jikji('tests/test_site/config2.json')
	model = jikji.model
	output_dir = jikji.config.path.output
	assets_dir = jikji.config.path.assets[0]


	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )

	jikji.generate()

	with open('%s/index.html' % output_dir, 'r') as file :
		content = file.read()


	assert model.cache.get( model.geturl('/users/Prev') ) is not None


	# TODO : Read With HTML Parser and check essential points
	assert content == """<!DOCTYPE html>
<html lang="en">
<head>
	<title>author</title>
</head>
<body>
	<div id="content">
<h1>Prev</h1>
<div>youngsoo lee</div>
<a href="https://api.github.com/users/Prev">Go github</a>
</div>
	<div id="footer">copyright prevdev@gmail.com</div>
</body>
</html>"""


	with open('%s/README.md' % output_dir, 'r') as f: c = f.read()
	with open('%s/README.md' % assets_dir, 'r') as f: c2 = f.read()
	assert c == c2


	with open('%s/css/stylesheet.css' % output_dir, 'r') as f: c = f.read()
	with open('%s/css/stylesheet.css' % assets_dir, 'r') as f: c2 = f.read()
	assert c == c2


