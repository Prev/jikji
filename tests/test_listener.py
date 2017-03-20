# -*- coding: utf-8 -*-
"""
	tests.listener
	---------------
	Test listener of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest

from jikji import Jikji
from jikji.listener import Listener


def test_listener1() :
	""" Testing for listening of testapp1
	"""
	app = Jikji('tests/testapp1')
	listener = Listener(app)

	for i in range(1, 5) :
		r = listener.response('/%s.html' % i)
		assert r[0] == '<div>%s</div>' % i




def test_listener2() :
	""" Testing for listening of testapp1
	"""

	app = Jikji('tests/testapp2')
	listener = Listener(app)
	
	r = listener.response('/')
	assert r[0] == '<p>Hello</p><i>home.html</i>'


	r = listener.response('/css/stylesheet.css')
	assert r[0] == b'html,body{ margin:0; padding:0 }'
	assert r[2]['Content-type'] == 'text/css'


	r = listener.response('/requirements.txt')
	assert r[0] == 'jikji>=2.0\nrequests>=2.11'
	assert r[2]['Content-type'] == 'text/plain'	

