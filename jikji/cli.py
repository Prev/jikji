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


cli_help = """
Static website generator based on RESTFul Server *~*

You can read guide from https://github.com/Prev/jikji

Example Usage:

   $ jikji <mysite> generate

"""



@click.group(help=cli_help)
@click.argument('sitepath', metavar='<sitepath>', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, sitepath) :
	ctx.obj['SITEPATH'] = sitepath



@cli.command('generate', short_help="Generate static site")
@click.pass_context
def generate_command(ctx) :
	""" Generate static site
	"""
	app = Jikji( ctx.obj['SITEPATH'] )
	app.generate()




@cli.command('clear')
@click.option('--cache', '-c', is_flag=True, default=False)
@click.option('--history', '-h', is_flag=True, default=False)
@click.pass_context
def clear_command(ctx, cache, history) :
	""" Clear cache or history created by jikji
	"""

	if cache:
		print('Clear cache')

	elif history:
		print('Clear history')

	else :
		print(ctx.get_help())






def main(as_module=False) :
	""" Main function called from shell or __main__.py
	
	:param as_module: True if called from __main__
	"""
	name = __package__

	if as_module :
		name = 'python -m ' + name

	cli(prog_name = name, obj={})

