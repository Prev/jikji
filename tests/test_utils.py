# -*- coding: utf-8 -*-
"""
	tests.utils
	---------------
	Test utils of application

	:author: Prev(prevdev@gmail.com)
"""

import pytest
import os.path

from jikji import Jikji
from jikji.utils import History


def test_cache() :
	jikji = Jikji('tests/test_site/config1.json')
	cache = jikji.cache

	cache.set('foo', 'bar')
	assert cache.get('foo') == 'bar'



def test_history() :
	jikji = Jikji('tests/test_site/config2.json')
	

	history = History(jikji.config)
	history.log('test', 'testval')


	with open(os.path.join(history.cur_historydir, 'test'), 'r') as file :
		content = file.read()


	assert content == 'testval'
	
