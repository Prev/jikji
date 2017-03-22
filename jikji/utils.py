"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""


def load_module(file_path, basepath=None) :
	""" Load python module by file path
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