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
from .utils import Cache
from .cprint import cprint

from . import __version__

class Jikji :

	def __init__(self, config_path) :
		self._conf = Config( config_path )
		self._cache = Cache(self._conf.sitepath)

		self._model = Model(
			server_info = self._conf.server_info,
			cache = self._cache
		)

		self._generator = Generator(
			config = self._conf,
			model = self._model
		)

	@property
	def config(self) :
		return self._conf


	@property
	def model(self) :
		return self._model


	@property
	def cache(self) :
		return self._cache

	@property
	def generator(self) :
		return self._generator


	def generate(self) :
		""" Generate static website
		"""
		cprint.line('Using Jikji %s ' % __version__)
		
		self._generator.generate()


