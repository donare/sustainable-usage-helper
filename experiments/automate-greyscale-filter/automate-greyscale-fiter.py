import winreg
import keyboard

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