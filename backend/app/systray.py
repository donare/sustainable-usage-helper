from os.path import abspath, join, dirname, isfile
from os import startfile
import threading
from PIL import Image

import pystray

from .globals import settings_file, icon_path, greyscale_worker_active
from .user import create_default, get_settings
from .greyscale import start_greyscale_worker, stop_greyscale_worker

def on_toggle(icon, item):
    if not item.checked: # if it was not checked
        start_greyscale_worker()
    else:
        stop_greyscale_worker()


def on_settings(icon, item):
    create_default(overwrite=False)

    startfile(settings_file)

def on_quit(icon, item):
    icon.stop()

def create_menu():
    menu_item_toggle = pystray.MenuItem(text="Enable/Disable Automatic Greyscale", action=on_toggle, checked=lambda item: greyscale_worker_active.is_set())

    menu_item_settings = pystray.MenuItem(text="Edit Settings", action=on_settings)

    menu_item_quit = pystray.MenuItem(text="Quit", action=on_quit)

    return pystray.Menu(menu_item_toggle, menu_item_settings, menu_item_quit)

def start_tray():           
    tray = pystray.Icon(name='test name', icon=Image.open(icon_path), menu=create_menu())
    
    start_greyscale_worker()

    tray.run()
