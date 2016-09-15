# -*- coding: utf-8 -*-

import pytest

import os
import shutil
from jikji.app import Jikji


def test_generate() :
	j = Jikji('tests/files/config.json')
	output_dir = j.config().output_dir()

	if os.path.exists( output_dir ) :
		shutil.rmtree( output_dir )


	j.generate()

	for i in range(1, 5) :
		with open('%s/%s.html' % (output_dir, i), 'r') as file:
			content = file.read()

		assert content == '<div>%s</div>' % i