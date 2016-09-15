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


def test_generate() :
	jikji = Jikji('tests/test_site/config.json')
	output_dir = jikji.config().output_dir()

	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )

	jikji.generate()

	for i in range(1, 5) :
		with open('%s/%s.html' % (output_dir, i), 'r') as file:
			content = file.read()

		assert content == '<div>%s</div>' % i

