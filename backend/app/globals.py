from os import getenv, mkdir
from os.path import join, isdir

is_active = True

settings_dir = join(getenv("LOCALAPPDATA"), "sustainable-usage-helper")

if not isdir(settings_dir):
    mkdir(settings_dir)

settings_file = join(settings_dir, "settings.json")
