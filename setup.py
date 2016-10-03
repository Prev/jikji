from setuptools import setup

import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('jikji/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))


setup(
	name = 'jikji',
	packages = ['jikji'],
	version = version,
	description = 'Static website generator based on RESTFul Server',
	license = 'MIT',

	author = 'Youngsoo Lee',
	author_email = 'prevdev@gmail.com',
	
	url = 'https://github.com/Prev/jikji',
	keywords = ['jikji', 'static', 'websites' 'generator', 'jinja2'],

	install_requires=[
		'Jinja2>=2.4',
		'click>=5.0',
		'Flask>=0.10',
		'requests>=2.11',
		'py>=1.4',
	],

	classifiers=(
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	),

	entry_points={
		'console_scripts': [
			'jikji = jikji.cli:main',
		],
	},
)
