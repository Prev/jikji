import os

# Root Path of Application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path includes Template files
TEMPLATE_ROOT = ROOT_PATH + '/template'

# Directory that includes Static files (to copied to output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory that includes ViewModel files
VIEWMODEL_ROOT = ROOT_PATH + '/view-model'

# Directory that rendered output will be located
OUTPUT_ROOT = ROOT_PATH + '/output'




# File that declares views and pages
PAGES = ROOT_PATH + '/pages.py'
