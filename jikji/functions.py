# -*- coding: utf-8 -*-
"""
	jikji/functions
	----------------
	global functions used in jikji or template

	:author: Prev(prevdev@gmail.com)
"""
from collections import OrderedDict
from .cprint import cprint



def group(array, *args) :
	""" Group json object by property
	
	:param array: json parsed array
	:param **kwarg: gruoping properties
	"""

	# for data in array :
	#print(array)

	result = OrderedDict()

	for data in array :
		keys = []
		for arg in args :
			cur = data # current value of data (go deeply)
			for property in arg :
				cur = cur[property]
			keys.append(cur) # find value in data by args

		cur = result
		for index, key in enumerate(keys) :
			# init cur[key] if not exists
			if key not in cur :
				if index == len(keys) - 1:	cur[key] = [] # init to array if key is lastest
				else :						cur[key] = OrderedDict()
			
			cur = cur[key] # go deeply

		cur.append(data)

	return result