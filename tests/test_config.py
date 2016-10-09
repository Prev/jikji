# -*- coding: utf-8 -*-
"""
	tests.config
	---------------
	Test config of application

	:author: Prev(prevdev@gmail.com)
"""


import pytest
import os.path

from jikji import Jikji



def test_config1() :
	basedir = os.path.join('tests', 'test_site')

	jikji = Jikji(os.path.join(basedir, 'config1.json'))
	config = jikji.config

	assert config.path.tpl == os.path.join(basedir, 'templates')
	assert config.path.output == os.path.join(basedir, 'generated', '1')
	assert config.path.pages_xml == os.path.join(basedir, 'pages1.xml')
	assert config.path.assets == [os.path.join(basedir, 'assets')]

	assert config.server_info['base_url'] == 'http://echo.jsontest.com'
	assert config.log_history == False


	assert config.imports == []


def test_config2() :
	jikji = Jikji(os.path.join('tests', 'test_site', 'config2.json'))
	config = jikji.config

	assert config.path.assets == []

	assert config.imports == ["time", ["datetime", "datetime"]]