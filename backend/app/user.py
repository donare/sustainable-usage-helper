import sys
from os.path import isfile
import json
import datetime
from .globals import settings_file

default_settings = {
    "block_start": "23:00",
    "block_end": "07:00"
}

def create_default(overwrite=False):
    if overwrite or not isfile(settings_file):
        with open(settings_file, "w") as file:
            json.dump(default_settings, file)

with open(settings_file, "r") as file:
    settings = json.loads(file.read())

print(settings)
