from os.path import abspath, join, dirname, isfile
from os import startfile
from PIL import Image

import pystray

from .globals import is_active, settings_file
from .user import create_default


def on_toggle(icon, item):
    global is_active
    is_active = not item.checked

def on_settings(icon, item):
    create_default(overwrite=False)

    startfile(settings_file)

def on_quit(icon, item):
    icon.stop()

def create_menu():
    menu_item_toggle = pystray.MenuItem(text="Enable/Disable Greyscale", action=on_toggle, checked=lambda item: is_active)

    menu_item_settings = pystray.MenuItem(text="Edit Settings", action=on_settings)

    menu_item_quit = pystray.MenuItem(text="Quit", action=on_quit)

    return pystray.Menu(menu_item_toggle, menu_item_settings, menu_item_quit)

def start_tray():
    icon_path = abspath(join(dirname(__file__), 'icon.png')) 
            
    tray = pystray.Icon(name='test name', icon=Image.open(icon_path), menu=create_menu())
    
    tray.run()
