# -*- coding: utf-8 -*-
"""
	jikji/app
	----------------
	Jikji class implements

	:author: Prev(prevdev@gmail.com)
"""

import os

from .config import Config
from .model import Model
from .generator import Generator


class Jikji :

	def __init__(self, config_path) :
		self._conf = Config( config_path )
		self._model = Model( self._conf.rest_server_info() )

		self.generator = Generator(self._conf, self._model)
	

	def config(self) :
		return self._conf


	def model(self) :
		return self._model


	def generate(self) :
		self.generator.generate()

