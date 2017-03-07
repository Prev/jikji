"""
	Jikji/cli
	----------------
	Command line application for jikji app.
	
	:author: Prev(prevdev@gmail.com)
	
"""

import sys
import click

from .app import Jikji
#from .listener import Listener


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
	r = app.generate()
	
	sys.exit(r)




def main(as_module=False) :
	""" Main function called from shell or __main__.py
	
	:param as_module: True if called from __main__
	"""
	name = __package__

	if as_module :
		name = 'python -m ' + name

	cli(prog_name = name, obj={})

