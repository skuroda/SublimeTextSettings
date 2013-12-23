# Adapted from @wbond's resource loader.

import sys
import sublime

VERSION = int(sublime.version())

mod_prefix = "utilities"
reload_mods = []

if VERSION > 3000:
    mod_prefix = "User." + mod_prefix
    from imp import reload

    for mod in sys.modules:
        if mod[0:4] == 'User' and sys.modules[mod] is not None:
            reload_mods.append(mod)
else:
    for mod in sorted(sys.modules):
        if mod[0:9] == 'utilities' and sys.modules[mod] is not None:
            reload_mods.append(mod)

mods_load_order = [
    '.expand_setting_env_vars',
    '.window_navigation',
    '.split_line',
    '.keyboard_multicursor',
    '.view_navigation',
    ''
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        print(mod)
        reload(sys.modules[mod])
