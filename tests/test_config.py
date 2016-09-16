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
	config = jikji.config()

	assert config.tpl_dir() == 'tests/test_site/templates'
	assert config.output_dir() == 'tests/test_site/generated/1'
	assert config.pages_xml_path() == 'tests/test_site/pages1.xml'
	assert config.rest_server_info()['base_url'] == 'https://test.com/'

