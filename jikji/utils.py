"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""

import re

def load_module(file_path, basepath=None) :
	""" Load python module by file path

	:param file_path: Location of loading file
	:param basepath: Used in Parsing module name to be put in sys.modules
	"""
	import os, sys, importlib
	
	module_name = os.path.basename(file_path)
	if module_name[-3:] == '.py' :
		module_name = module_name[:-3]

	if basepath :
		sys_module_dir = os.path.relpath(
			os.path.dirname(file_path), basepath
		).replace('/', '.').replace('\\', '.')

		if sys_module_dir[0] == '.' :
			sys_module_dir = sys_module_dir[1:]

		sys_module_name = sys_module_dir + '.' + module_name
	else :
		sys_module_name = module_name


	if sys.version_info >= (3, 5) :
		# For python 3.5+
		spec = importlib.util.spec_from_file_location(module_name, file_path)
		module = importlib.util.module_from_spec(spec)

		sys.modules[sys_module_name] = module
		sys.modules[module_name] = module
		spec.loader.exec_module(module)
		

	else :
		# For python 3.3 and 3.4
		from importlib.machinery import SourceFileLoader
		module = SourceFileLoader(module_name, file_path).load_module()
		sys.modules[sys_module_name] = module

	return module



def getprop(data, property_name) :
	""" Get property from dict or class

	:param data: dict, list, tuple or class
	:param property_name: Name of property
						  You can use '$n' syntax to access list item by index
	"""

	if '.' in property_name :
		l = property_name.split('.')
		pn = l.pop(0)
		return getprop(
			getprop(data, pn),
			'.'.join(l)
		)

	if property_name[0] == '$' :
		property_name = int(property_name[1:]) - 1

	try :
		d = getattr(data, property_name)
	except KeyError :
		return None
	except (AttributeError, TypeError) :
		try :
			d = data.__getitem__(property_name)
		except (AttributeError, KeyError, TypeError) :
			return None
	return d


pvs_re = re.compile(r'([^\\])({\s*([a-zA-Z0-9-_$\.]+)\s*})')
pvs_re2 = re.compile(r'()()(\$[0-9]+)')

def parse_varstr(rulestr, data) :
	""" Parse var in string. Var data is given by dict param
		ex) parse_varstr('/posts/{post_id}', {'post_id': 3}) // returns "/posts/3"
			parse_varstr('/posts/$1/$2', ['Category1', 'My-Post']) // returns "/posts/Category1/My-Post"

	:param rulestr: Ruled string to be replaced
	:param data:	Data variable (dict, list, tuple or class)
	"""
	def pvs_callback(m) :
		varid = m.group(3)
		d = getprop(data, varid)

		return "%s%s" % (m.group(1), d)

	rv = pvs_re.sub(pvs_callback, rulestr)
	rv = rv.replace('\\{', '{')
	rv = pvs_re2.sub(pvs_callback, rv)
	return rv


