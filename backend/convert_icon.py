#!/usr/bin/env python3

from PIL import Image

icon = Image.open("icon.png")
icon.save("icon.ico")
