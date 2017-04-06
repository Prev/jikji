"""
	Jikji
	----------------
	Static website generator adapting View-ViewModel Pattern 
	
	:author: Prev(prevdev@gmail.com)
	:license: MIT

"""

__version__ = '2.0.2-beta'

from jikji.app import Jikji, addpage, getview
from jikji.view import render_template, register_view