"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""

import re, os, shutil

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





def copytree2(src, dst, ignore_hidden=True,
				callback_before=None, callback_after=None, dir=None) :
		""" Copy files recursively
		
		:params
			- src: Source dir to copy
			- dst: Destiny root dir that copied file will located to
			- ignore_hidden: Ignore hidden files
			- callback_before: Callback function before file copied (If return value is False, do not copy)
			- callback_after: Callback function after file copied
			- dir: Directory path for recursively explored (if value is None, use src for first call)
		"""
		
		if dir is None : dir = src
		if not os.path.isdir(dir) : return

		list = os.listdir(dir)
		
		for file in list :
			if ignore_hidden and file[0] == '.' :
				# continue if file is hidden
				continue

			filepath = os.path.join(dir, file)

			if os.path.isdir(filepath) :
				# if file is directory, call function recursively
				copytree2(src, dst, ignore_hidden, callback_before, callback_after, filepath)

			else :
				# filepath that common string of src is removed
				trimed_path = filepath[ len(src)+1 : ] 
				dst_path = os.path.join(dst, trimed_path)

				if callback_before :
					rv = callback_before(trimed_path, filepath)
					if rv == False :
						continue

				os.makedirs( os.path.dirname(dst_path), exist_ok=True )
				shutil.copy2(
					src = filepath,
					dst = dst_path
				)

				if callback_after :
					callback_after(trimed_path, filepath)
				
				#cprint.line('/%s [Asset]' % trimed_path)

