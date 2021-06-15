import sys
from PIL import Image

import pystray

is_active = True

def on_toggle(icon, item):
    global is_active
    is_active = not item.checked

def on_quit(icon, item):
    icon.stop()

menu_item_toggle = pystray.MenuItem(text="Enable/Disable Greyscale", action=on_toggle, checked=lambda item: is_active)

menu_item_quit = pystray.MenuItem(text="Quit", action=on_quit)

menu = pystray.Menu(menu_item_toggle, menu_item_quit)

icon = pystray.Icon(name='test name', icon=Image.open("icon.png"), menu=menu).run()

