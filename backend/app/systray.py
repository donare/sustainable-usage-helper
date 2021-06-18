from os.path import abspath, join, dirname
from PIL import Image

import pystray

from .globals import is_active


def on_toggle(icon, item):
    global is_active
    is_active = not item.checked

def on_quit(icon, item):
    icon.stop()

def create_menu():
    menu_item_toggle = pystray.MenuItem(text="Enable/Disable Greyscale", action=on_toggle, checked=lambda item: is_active)

    menu_item_quit = pystray.MenuItem(text="Quit", action=on_quit)

    return pystray.Menu(menu_item_toggle, menu_item_quit)


def start_tray():
    icon_path = abspath(join(dirname(__file__), 'icon.png')) 
            
    tray = pystray.Icon(name='test name', icon=Image.open(icon_path), menu=create_menu())
    
    tray.run()
