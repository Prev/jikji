"""
	Jikji
	----------------
	Python Static website generator for Modern web
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT

"""

__version__ = '2.1.4'

from .app import Jikji, addpage, addpagegroup, getview
from .view import render_template, register_view