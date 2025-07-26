import os

def getthumb():
    path = "thumb.jpg"  # or "/bot/thumb.jpg" if absolute is needed
    return path if os.path.exists(path) else None
