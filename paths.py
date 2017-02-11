import os.path

# App root for misc file retrieval
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Location for all app input and output files
DATA_DIR = os.path.join(APP_ROOT, 'data')

# Directory where lyric sets will be stored.
LYRICS_SETS = os.path.join(DATA_DIR, 'lyrics-sets')

# Directory for app resources (config etc.)
APP_RESOURCES = os.path.join(APP_ROOT, *['app', 'resources'])

# File for various logs
APP_LOGS = os.path.join(APP_ROOT, *['app', 'logs'])

