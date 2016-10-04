# -*- coding: utf-8 -*-
"""
	Jikji/cli
	----------------
	Command line application for jikji app.
	
	:author: Prev(prevdev@gmail.com)
	
"""

import sys
import click

from .app import Jikji
from .cprint import cprint
from .listener import Listener


cli_help = """\
\b
Static website generator based on RESTFul Server *~*
You can read guide from https://github.com/Prev/jikji

\b 
Example Usage:
   $ jikji <mysite> generate
   $ jikji <mysite> cache list

"""



@click.group(help=cli_help)
@click.argument('sitepath', metavar='<sitepath>', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, sitepath) :
	ctx.obj['SITEPATH'] = sitepath
	ctx.obj['APP'] = Jikji( sitepath )



"""
Command for generate
Usage:
	jikji <sitepath> generate

"""
@cli.command('generate', short_help="Generate static site")
@click.pass_context
def generate_command(ctx) :
	""" Generate static site
	"""
	app = ctx.obj['APP']
	app.generate()




"""
Command for cache
Usage:
	jikji <sitepath> cache <command> [--Args] [--Options]

"""
@cli.group('cache', help="Manage Cache")
def cache() :
	pass

@cache.command('list', short_help="Listing caches")
@click.pass_context
def cache_list_command(ctx) :
	app = ctx.obj['APP']

	for file in app.cache.list(details=True) :
		print(file)


@cache.command('clear', short_help="Remove all cache files")
@click.pass_context
def cache_clear_command(ctx) :
	app = ctx.obj['APP']
	app.cache.remove_all()

@cache.command('remove', short_help="Remove cache file matched")
@click.argument('key', metavar='<key>')
@click.option('--regex', '-r', is_flag=True, default=False, help="Using regex match instead of string equal")
@click.pass_context
def cache_remove_command(ctx, key, regex) :
	app = ctx.obj['APP']
	app.cache.remove(key, as_pattern=regex)




"""
Open listening server for develop
Usage:
	jikji <sitepath> listen

"""
@cli.command('listen')
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--port', '-p', default=7000)
@click.pass_context
def listen_command(ctx, host, port) :
	""" Generate static site
	"""
	app = ctx.obj['APP']

	listener = Listener(app)
	listener.listen(host=host, port=port)



def main(as_module=False) :
	""" Main function called from shell or __main__.py
	
	:param as_module: True if called from __main__
	"""
	name = __package__

	if as_module :
		name = 'python -m ' + name

	cli(prog_name = name, obj={})

