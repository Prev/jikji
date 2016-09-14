#-*- coding: utf-8 -*-

import os

from config import Config
from model import Model
from generator import Generator


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def run() :
	conf = Config(BASE_DIR + '/../sample_site/config.json')
	model = Model(conf.rest_server_info())

	g = Generator(conf, model)
	g.generate()



if __name__ == '__main__' :
	run()