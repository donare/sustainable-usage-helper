import sys
from os.path import join, abspath, dirname, isdir, isfile
from os import getenv, mkdir
from PIL import Image
import json
import datetime

settings_dir = join(getenv("LOCALAPPDATA"), "sustainable-usage-helper")

if not isdir(settings_dir):
    mkdir(settings_dir)

settings_file = join(settings_dir, "settings.json")

default_settings = {
    "block_start": "23:00",
    "block_end": "07:00"
}

if not isfile(settings_file):
    with open(settings_file, "w") as file:
        json.dump(default_settings, file)

with open(settings_file, "r") as file:
    settings = json.loads(file.read())

print(settings)
