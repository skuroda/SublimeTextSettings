
import sublime
import sys
import os

VERSION = int(sublime.version())

# Expand settings
def expand_settings():
    for filename, setting_keys in expand_settings.items():
        s = sublime.load_settings(filename)
        for key in setting_keys:
            value = s.get(key)
            if value is not None:
                s.set(key, os.path.expandvars(value))

def plugin_loaded():
    expand_settings()

if VERSION < 3006:
    expand_settings()


# Load utility plugins
reloader = "utilities.reloader"

if VERSION > 3000:
    reloader = 'User.' + reloader
    from imp import reload


# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
    reload(sys.modules[reloader])

if VERSION > 3000:
    from .utilities import reloader
    from .utilities import *
else:
    from utilities import reloader
    from utilities import *



