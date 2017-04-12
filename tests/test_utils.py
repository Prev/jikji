"""
	tests.utils
	---------------
	Test listener of application

	:author: Prev(prevdev@gmail.com)
"""

from jikji import utils


def test_getprop() :
	class TestClass :
		def __init__(self) :
			self.a = 3

	assert utils.getprop({'a': 1}, 'a') == 1
	assert utils.getprop({'a': 1}, 'b') == None
	assert utils.getprop(TestClass(), 'a') == 3
	assert utils.getprop(TestClass(), 'b') == None

	assert utils.getprop({'c': {'d': 5}}, 'c.d') == 5
	assert utils.getprop({'c': {'d': 5}}, 'c.e') == None

	assert utils.getprop(['X', 'Y', 'Z'], '$1') == 'X'
	assert utils.getprop({'arr': ['X', 'Y', 'Z']}, 'arr.$2') == 'Y'
	assert utils.getprop([{'a': 1}, {'b': 2}], '$1.a') == 1


def test_parse_varstr() :
	""" Test utils.parse_varstr
	"""
	assert utils.parse_varstr('/posts/{ board_id }/{post_id}', data={
		'board_id': 'free',
		'post_id': 33,
	}) == '/posts/free/33'


	assert utils.parse_varstr('/{ myvar1 }?json=\{"a": 1}', data={
		'myvar1': 4
	}) == '/4?json={"a": 1}'


	class TestClass :
		def __init__(self) :
			self.a = 1

	assert utils.parse_varstr('/{ a }/', data=TestClass()) == '/1/'


	assert utils.parse_varstr('/$1/$2', data=[
		'Category1',
		'Article1',
	]) == '/Category1/Article1'

	assert utils.parse_varstr('/{ $1.id }/{ $2.id }', data=[
		{'id': 'Category1'},
		{'id': 'Article1'},
	]) == '/Category1/Article1'



