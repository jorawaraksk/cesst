# https://github.com/1Danish-00/CompressorQueue/blob/main/License

from telethon import Button
from .worker import *
from datetime import datetime

START_TIME = datetime.now()

# Optional: Define ts() if not defined elsewhere
def ts(ms):
    # Simple time formatting for uptime
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"Uptime: {hours:02}:{minutes:02}:{seconds:02}"

async def up(event):
    if not event.is_private:
        return
    stt = datetime.now()
    ed = datetime.now()
    v = ts(int((ed - START_TIME).seconds) * 1000)
    ms = (ed - stt).microseconds / 1000
    p = f"Ping = {ms}ms"
    await event.reply(v + "\n" + p)


async def start(event):
    await event.reply(
        f"**Send me the video which you want to compress.**\n**Uptime: {str(datetime.now() - START_TIME).split('.')[0]}**",
        buttons=[
            [Button.inline("HELP", data="help")],
        ],
    )


async def zylern(event):
    await event.reply(
        f"""
**Available Commands 😉**

/start - __Check Bot is Working Or Not__
/help - __Get Detailed Help__
/setcode - __Set Custom FFMPEG Code__
/getcode - __Print Current FFMPEG Code__
/logs - __Get Bot Logs__
/ping - __Check Ping__
/sysinfo - __Get System Info__
/renew - __Clear Cached Downloads__
/clear - __Clear Queued Files__
/showthumb - __Show Current Thumbnail__
/cmds - __List Available Commands__
"""
    )


async def help(event):
    await event.edit(
        f"""**To check current ffmpeg code you can use** /getcode\n\n**You can change your ffmpeg code by executing following command.**\n\n`/setcode -preset faster -c:v libx265 -s 1280x720 -x265-params 'bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1' -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 1`\n\n**To set custom thumbnail send me the image.**\n\n**Do /cmds For More**"""
    )


async def ihelp(e):
    await e.reply(
        f"""**To check current ffmpeg code you can use** /getcode\n\n**You can change your ffmpeg code by executing following command.**\n\n`/setcode -preset faster -c:v libx265 -s 1280x720 -x265-params 'bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1' -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 1`\n\n**To set custom thumbnail send me the image.**\n\n**Do /cmds For More**"""
    )
