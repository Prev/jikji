# -*- coding: utf-8 -*-
"""
	jikji/app
	----------------
	Jikji class implements

	:author: Prev(prevdev@gmail.com)
"""

import os

from .config import Config
from .model import Model, Cache
from .generator import Generator
from .history import History

from . import __version__
from . import cprint

class Jikji :

	def __init__(self, config_path) :
		self._conf = Config( config_path )
		self._history = History( self._conf )
		self._cache = Cache(self._conf.sitepath)

		self._model = Model(
			server_info = self._conf.server_info,
			cache = self._cache
		)

		self._generator = Generator(
			configpath = self._conf.path,
			model = self._model,
			history = self._history
		)
		


	@property
	def config(self) :
		return self._conf


	@property
	def model(self) :
		return self._model


	def generate(self) :
		cprint.line('Using Jikji %s ' % __version__)
		
		self._generator.generate()
