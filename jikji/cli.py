"""
	Jikji/cli
	----------------
	Command line application for jikji app.
	
	:author: Prev(prevdev@gmail.com)
	
"""

import sys
import click

from . import __version__
from .app import Jikji
from .generator import Generator
from .listener import Listener


cli_help = """\
\b
Jikji """ + __version__ + """

Python Static website generator for Modern web *~*
You can read guide from https://github.com/Prev/jikji

\b 
Example Usage:
   $ jikji <mysite> generate
   $ jikji -o initialize <mysite> generate
   $ jikji --option development <mysite> generate
   $ jikji <mysite> listen

"""



@click.group(help=cli_help)
@click.option('--options', '-o', default='')
@click.argument('sitepath', metavar='<sitepath>', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, sitepath, options) :
	ctx.obj['SITEPATH'] = sitepath
	ctx.obj['APP'] = Jikji(sitepath=sitepath, options=options.split(','))



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
	""" Open listening server for develop
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

