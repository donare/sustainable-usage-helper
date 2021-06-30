import sys
from os.path import isfile
import json
from datetime import time
from .globals import settings_file
from win10toast import ToastNotifier

default_settings = {
    "block_start": "23:00",
    "block_end": "07:00"
}

def create_default(overwrite=False):
    if overwrite or not isfile(settings_file):
        with open(settings_file, "w") as file:
            json.dump(default_settings, file)

def get_settings():
    create_default(overwrite=False)

    with open(settings_file, "r") as file:
        settings = json.loads(file.read())

    if not all(key in settings for key in ["block_start", "block_end"]):
        n = ToastNotifier()

        n.show_toast("Settings Error", "The Setings file does not conatain the necessary keys", duration=10)

        return

    for key in ['block_start', 'block_end']:
        settings[key] = time.fromisoformat(settings[key])

    return settings

