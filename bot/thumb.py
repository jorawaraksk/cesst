# bot/thumb.py

import os

def getthumb(event=None):
    # Future support: per-user thumbnails
    path = "thumb.jpg"
    return path if os.path.exists(path) else None
