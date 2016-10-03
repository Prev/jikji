# -*- coding: utf-8 -*-
"""
	tests.model
	---------------
	Test model of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest
import flask

from jikji import Jikji
from jikji.model import ModelException


def test_cache() :
	jikji = Jikji('tests/test_site/config1.json')
	model = jikji.model

	model.cache.set('foo', 'bar')
	assert model.cache.get('foo') == 'bar'



def test_model1() :
	jikji = Jikji('tests/test_site/config1.json')
	model = jikji.model
	
	assert model.get('/foo/bar')['foo'] == 'bar'
	assert model.get('hello/world', None)['hello'] == 'world'
	assert model.get(
		api = 'hello/world/brave/new',
		immutable = True
	)['hello'] == 'world'
	


def test_model2() :
	jikji = Jikji('tests/test_site/config2.json')
	model = jikji.model
	
	try :
		model.get('/invalid_404_page')
	except ModelException as e :
		assert e.status == '404 NOT FOUND'

