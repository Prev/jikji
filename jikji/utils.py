"""
	jikji/utils
	----------------
	Utils of jikji

	:author: Prev(prevdev@gmail.com)
"""


def load_module(module_name, path='.') :
	import os, sys, importlib
	
	path = os.path.join(path, module_name + '.py')

	if sys.version_info >= (3, 5) :
		# For python 3.5+
		spec = importlib.util.spec_from_file_location(module_name, path)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		

	else :
		# For python 3.3 and 3.4
		from importlib.machinery import SourceFileLoader
		module = SourceFileLoader(module_name, path).load_module()

	return module