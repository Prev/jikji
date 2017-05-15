"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""

import re, os, shutil
import json
from urllib.parse import quote_plus, unquote_plus



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



class AppDataUtil :

	def __init__(self, app) :
		self.appdata_root = os.path.join(app.settings.ROOT_PATH, '.jikji')			

	def appdata_path(self, name) :
		return os.path.join(self.appdata_root, name)


class Cache(AppDataUtil) :

	def __init__(self, app) :
		""" Init Cache Class with app
		"""
		
		AppDataUtil.__init__(self, app)

		self.cachedir = self.appdata_path('cache')
		os.makedirs(self.cachedir, exist_ok=True )


	def getpath(self, key, quote=True) :
		""" Get cache file path of key
		"""
		if quote :
			key = quote_plus(key)
		else :
			dirname = os.path.dirname(key)
			dirpath = os.path.join(self.cachedir, dirname)

			if not os.path.isdir(dirpath) :
				os.makedirs(dirpath, exist_ok=True )

		return os.path.join(self.cachedir, key)


	def get(self, key, default=None, use_json=True, quote=True) :
		""" Get cached data with key
		If cache not found, return default value of param (default: None)
		"""
		cpath = self.getpath(key, quote)
		
		if os.path.isfile(cpath) :
			with open(cpath, 'r') as file:
				content = file.read()

			if content == '' and use_json :
				return default

			if use_json : return json.loads(content)
			else : 		  return content

		else :
			return default


	def set(self, key, value, use_json=True, quote=True) :
		""" Set cache data with key, value
		"""
		cpath = self.getpath(key, quote)

		if use_json :
			value = json.dumps(value)

		with open(cpath, 'w') as file:
			file.write( value )


	def list(self, details=False) :
		""" Listing cache files
		"""
		clist = os.listdir(self.cachedir)

		if details :
			nlist = []

			for file in clist :
				filepath = os.path.join(self.cachedir, file)
				nlist.append('%s (%s bytes)' % (unquote_plus(file), os.path.getsize(filepath) ) )

			return nlist

		else :
			return clist


	def remove(self, key, as_pattern=False) :
		""" Remove cache data
		:param key: Key for cache or pattern if as_pattern is True
		:param as_pattern: Remove caches that matches with 'key' as regex
		"""

		if not as_pattern :
			cpath = self.getpath(key)

			if os.path.isfile(cpath) :
				os.remove(cpath)
				cprint.line('Cache "%s" is removed' % key)
			else :
				cprint.error('Cache "%s" not exists' % key)


		else :
			r = re.compile(key)
			clist = self.list()

			something_removed = False

			for file in clist :
				filepath = os.path.join(self.cachedir, file)

				if r.match(filepath) is not None :
					os.remove(filepath)

					something_removed = True
					cprint.line('Removed: %s' % unquote_plus(file))

			if not something_removed :
				cprint.warn('No pattern matched file with "%s"' % key)


	def remove_all(self) :
		""" Remove all cache data
		"""
		self.remove('.*', as_pattern=True)

