"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""


def load_module(file_path) :
	import os, sys, importlib
	
	module_name = os.path.basename(file_path)
	if module_name[-3:] == '.py' :
		module_name = module_name[:-3]
		
	#path = os.path.join(path, module_name + '.py')

	if sys.version_info >= (3, 5) :
		# For python 3.5+
		spec = importlib.util.spec_from_file_location(module_name, file_path)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		

	else :
		# For python 3.3 and 3.4
		from importlib.machinery import SourceFileLoader
		module = SourceFileLoader(module_name, file_path).load_module()

	return module