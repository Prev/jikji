# -*- coding: utf-8 -*-
"""
	tests.model
	---------------
	Test model of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest

from jikji import Jikji
from jikji.model import ModelException


def test_model1() :
	jikji = Jikji('tests/test_site/config1.json')
	model = jikji.model
	
	# test get req
	assert model.get('/foo/bar')['foo'] == 'bar'
	assert model.get(
		api = 'hello/world/brave/new',
		immutable = True
	)['hello'] == 'world'
	


	# test form
	model.makeform(
		name = 'form1',
		method = 'GET',
		api = '/var1/$1/var2/$2'
	)

	r = model.form('form1', 'data1', 'data2')
	assert r['var1'] == 'data1'
	assert r['var2'] == 'data2'


	r = model.get('/', baseurl='http://ip.jsontest.com/')
	assert r['ip'] is not None



def test_model2() :
	jikji = Jikji('tests/test_site/config2.json')
	model = jikji.model
	
	# test exception handling
	try :
		model.get('/invalid_404_page')
	except ModelException as e :
		assert e.status == '404 NOT FOUND'

