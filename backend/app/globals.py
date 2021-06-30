from os import getenv, mkdir
from os.path import join, isdir, abspath, dirname
import threading

greyscale_worker_active = threading.Event()
greyscale_worker_active.set()

settings_dir = join(getenv("LOCALAPPDATA"), "sustainable-usage-helper")

if not isdir(settings_dir):
    mkdir(settings_dir)

settings_file = join(settings_dir, "settings.json")

icon_path = abspath(join(dirname(__file__), 'icon.png')) 