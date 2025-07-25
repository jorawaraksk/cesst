from decouple import config

try:
    APP_ID = config("APP_ID", "16732227")
    API_HASH = config("API_HASH", "8b5594ad7ad37f3a0a7ddbfb3963bb51")
    BOT_TOKEN = config("BOT_TOKEN", "7141984677:AAFztMNvuW-CYbsM1Ydq0zTZ6OQumWSEHTs")
    DEV = 5868426717
    OWNER = config("OWNER", "5868426717").split()
    PUBLIC = config("PUBLIC", default=True, cast=bool)
    ffmpegcode = ["-preset veryfast -c:v libx265 -b:a 64k -crf 38 -map 0 -c:s copy"]
    THUMB = config("THUMB", "https://static7.depositphotos.com/1009183/713/i/950/depositphotos_7132926-stock-photo-beautiful-tree-in-the-sunset.jpg")
except Exception as e:
    print("Environment vars Missing")
    print(str(e))
    exit(1)
