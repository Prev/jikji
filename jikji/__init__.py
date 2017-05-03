"""
	Jikji
	----------------
	Static website generator adapting View-ViewModel Pattern 
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT

"""

__version__ = '2.1.0-r1'

from .app import Jikji, addpage, addpagegroup, getview
from .view import render_template, register_view