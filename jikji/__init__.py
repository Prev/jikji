"""
	Jikji
	----------------
	Static website generator adapting View-ViewModel Pattern 
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT

"""

__version__ = '2.0.0'

from .app import Jikji, addpage, addpagegroup, getview
from .view import render_template, register_view