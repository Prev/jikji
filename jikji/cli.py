"""
	Jikji/cli
	----------------
	Command line application for jikji app.
	
	:author: Prev(prevdev@gmail.com)
	
"""

import sys
import shutil
import os.path
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
   $ jikji create <project_dir>
   $ jikji generate <project_dir> --options [options]
   $ jikji listen <project_dir> --options [options] --host [host] --port [port]

"""



@click.group(help=cli_help)
def cli():
	pass

@cli.command('create', help=cli_help)
@click.argument('proj_dir', metavar='<proj_dir>')
def create_command(proj_dir):
	if os.path.isfile(proj_dir + '/settings.py'):
		print('It seems like there is a project on %s' % proj_dir)
		sys.exit(-1)

	print(os.path.dirname(__file__) + '/sample_proj', proj_dir)
	shutil.copytree(os.path.dirname(__file__) + '/sample_proj', proj_dir)


@cli.command('generate', help=cli_help)
@click.argument('proj_dir', metavar='<proj_dir>', type=click.Path(exists=True))
@click.option('--options', '-o', default='')
def generate_command(proj_dir, options):
	app = Jikji(sitepath=proj_dir, options=options.split(','))
	r = app.generate()
	sys.exit(r)


@cli.command('listen')
@click.argument('proj_dir', metavar='<proj_dir>', type=click.Path(exists=True))
@click.option('--options', '-o', default='')
@click.option('--host', '-h', default='0.0.0.0')
@click.option('--port', '-p', default=7000)
def listen_command(proj_dir, options, host, port):
	app = Jikji(sitepath=proj_dir, options=options.split(','))
	listener = Listener(app)
	listener.listen(host=host, port=port)


def main(as_module=False):
	""" Main function called from shell or __main__.py
	:param as_module: True if called from __main__
	"""
	name = __package__

	if as_module :
		name = 'python -m ' + name

	cli(prog_name = name, obj={})

