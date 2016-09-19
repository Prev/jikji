from setuptools import setup

setup(
	name = 'jikji',
	packages = ['jikji'],
	version = '0.1.2',
	description = 'Code-less static web generator based on RESTFul API Server',
	license = 'MIT',

	author = 'Youngsoo Lee',
	author_email = 'prevdev@gmail.com',
	
	url = 'https://github.com/Prev/jikji',
	keywords = ['static-web', 'generator'],

	install_requires=[
		'Jinja2>=2.4',
		'requests>=2.11',
		'py>=1.4',
	],
)