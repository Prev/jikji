import os

# Root Path of Application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path includes Template files
TEMPLATE_ROOT = ROOT_PATH + '/templates'

# Directory that includes Static files (to copied to output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory that includes View files
VIEW_ROOT = ROOT_PATH + '/views'

# Directory that rendered output will be located
OUTPUT_ROOT = ROOT_PATH + '/output'




# Scripts that runned on initializing application
INIT_SCRIPTS = (
	ROOT_PATH + '/app.py',
)
