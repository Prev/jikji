# -*- coding: utf-8 -*-
"""
	tests.model
	---------------
	Test model of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest

from jikji import Jikji



def test_model() :
	jikji = Jikji('tests/test_site/config.json')
	
	model = jikji.model()

	model.set_baseurl('https://api.github.com/')
	assert model.get('/users/Prev')['login'] == 'Prev'

	model.set_baseurl('https://api.github.com')
	assert model.get('/users/Prev')['login'] == 'Prev'
	
print('hi')
test_model()