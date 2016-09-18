# -*- coding: utf-8 -*-
"""
	tests.config
	---------------
	Test config of application

	:author: Prev(prevdev@gmail.com)
"""


import pytest

from jikji import Jikji



def test_config() :
	jikji = Jikji('tests/test_site/config1.json')
	config = jikji.config

	assert config.path.tpl == 'tests/test_site/templates'
	assert config.path.output == 'tests/test_site/generated/1'
	assert config.path.pages_xml == 'tests/test_site/pages1.xml'
	
	assert config.server_info['base_url'] == 'http://echo.jsontest.com'

