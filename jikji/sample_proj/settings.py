import os
from jikji.publisher import LocalPublisher

# Root path of the application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path for template files.
# Jikji use jinja2 engine on rendering templates, which is used on Flask.
# It means that you can use full syntax of Flask, including layout and macro features.
TEMPLATE_ROOT = ROOT_PATH + '/templates'

# Directory for static files (to be copied to the output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory for view files
VIEW_ROOT = ROOT_PATH + '/views'

# Publisher instance used after generation
PUBLISHER = LocalPublisher(output_root=ROOT_PATH + '/output')
# PUBLISHER = S3Publisher('my-bucket1')


# Scripts to be run on initialization process
# You can separate data fetching process, defining url rules, or others.
INIT_SCRIPTS = (
	ROOT_PATH + '/pages.py',
)
