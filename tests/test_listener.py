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
	app = Jikji('tests/test_site/config1.json')
	listener = Listener(app)

	for i in range(1, 5) :
		r = listener.response('/%s.html' % i)
		assert r[0] == '<div>%s</div>' % i


	r = listener.response('/')
	assert r[0] == '<p>Hello</p>'


	r = listener.response('/css/stylesheet.css')
	assert r[0] == b'html,body{ margin:0; padding:0 }'

