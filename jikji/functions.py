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



def strftime(timestamp, format) :
	""" Format timestamp to string

	:param timestamp: timestamp int (if timestamp is larger than 10^12, divide by 1000)
	:param format: format param put in datetime.stftime
	"""
	from datetime import datetime

	if timestamp >= pow(10, 12) :
		timestamp = timestamp / 1000.0

	d = datetime.fromtimestamp(timestamp)
	return d.strftime(format)