import winreg
import keyboard
import threading
from datetime import datetime

from .user import get_settings
from .globals import greyscale_worker_active

def is_greyscale_active():
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    regkey = winreg.OpenKey(registry, "SOFTWARE\Microsoft\ColorFiltering", access=winreg.KEY_READ)

    return bool(winreg.QueryValueEx(regkey, "Active")[0])


def toggle_greyscale():
    keyboard.send("ctrl+windows+c")


def set_greyscale_on():
    if not is_greyscale_active():
        toggle_greyscale()


def set_greyscale_off():
    if is_greyscale_active():
        toggle_greyscale()


def greyscale_worker(is_active):
    if not is_active.is_set():
        return

    settings = get_settings()

    current_time = datetime.now().time()

    if settings['block_start'] > settings['block_end']:
        if current_time > settings['block_start'] or \
            current_time < settings['block_end']:
            set_greyscale_on()
        else:
            set_greyscale_off()
    elif settings['block_end'] > current_time > settings['block_start']:
        set_greyscale_on()
    else:
        set_greyscale_off()
    
    if is_active.is_set():
        print("Greyscale is set")
    else:
        print("Greyscale is not set")

    if is_active.is_set():
        threading.Timer(10, greyscale_worker, [is_active]).start()

def start_greyscale_worker():
    greyscale_worker_active.set()
    threading.Thread(target=greyscale_worker, daemon=True, args=[greyscale_worker_active]).start()

def stop_greyscale_worker():
    greyscale_worker_active.clear()
