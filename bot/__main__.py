import os
import re
import logging
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# Internal modules
from .config import API_ID, API_HASH, BOT_TOKEN
from .worker import stats, skip
from .devtools import eval, bash
from .FastTelethon import *
from .funcn import is_authorized, is_owner, save_mode, IS_PUBLIC
from .stuff import start, zylern, up, ihelp, help as help_cb
from .stuff import coding, getcode
from .system import sysinfo, clearqueue, renew
from .thumb import getthumb
from .logs import getlogs
from .worker import dl_link
from .speed import test
from .worker import encod

LOGS = logging.getLogger("bot")
LOGS.setLevel(logging.INFO)

# Initialize bot with safe session handling
LOGS.info("Starting...")

try:
    bot = TelegramClient("bot", API_ID, API_HASH)
except Exception as e:
    LOGS.error("Session init failed. Deleting old session file.")
    try:
        os.remove("bot.session")
    except FileNotFoundError:
        LOGS.warning("No session file found to delete.")
    bot = TelegramClient("bot", API_ID, API_HASH)

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.error(f"Bot start failed: {er}")
    raise

########## COMMANDS ##########

@bot.on(events.NewMessage(pattern="/start"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await start(e)

@bot.on(events.NewMessage(pattern="/setcode"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to use this command.")
    await coding(e)

@bot.on(events.NewMessage(pattern="/getcode"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await getcode(e)

@bot.on(events.NewMessage(pattern="/showthumb"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 Only the owner can access the thumbnail.")
    await getthumb(e)

@bot.on(events.NewMessage(pattern="/logs"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to access logs.")
    await getlogs(e)

@bot.on(events.NewMessage(pattern="/cmds"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await zylern(e)

@bot.on(events.NewMessage(pattern="/ping"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await up(e)

@bot.on(events.NewMessage(pattern="/sysinfo"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to use this command.")
    await sysinfo(e)

@bot.on(events.NewMessage(pattern="/leech"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await dl_link(e)

@bot.on(events.NewMessage(pattern="/help"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await ihelp(e)

@bot.on(events.NewMessage(pattern="/renew"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to use this command.")
    await renew(e)

@bot.on(events.NewMessage(pattern="/clear"))
async def _(e):
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to use this command.")
    await clearqueue(e)

@bot.on(events.NewMessage(pattern="/speed"))
async def _(e):
    if not is_authorized(e.sender_id):
        return await e.reply("**Sorry You're not An Authorised User!**")
    await test(e)

########## ADVANCED ##########

@bot.on(events.NewMessage(pattern="/eval"))
async def _(e):
    await eval(e)

@bot.on(events.NewMessage(pattern="/bash"))
async def _(e):
    await bash(e)

########## CALLBACKS ##########

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile("help")))
async def _(e):
    await help_cb(e)

########## THUMBNAIL SETTER ##########

@bot.on(events.NewMessage(incoming=True))
async def _(event):
    if not is_owner(event.sender_id):
        return await event.reply("**Only OWNER can set thumbnail.**")
    if not event.photo:
        return
    os.system("rm thumb.jpg")
    await event.client.download_media(event.media, file="/bot/thumb.jpg")
    await event.reply("**Thumbnail Saved Successfully.**")

########## FILE HANDLER ##########

@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await encod(e)

########## TOGGLE PUBLIC/PRIVATE ##########

@bot.on(events.NewMessage(pattern="/mode"))
async def _(e):
    global IS_PUBLIC
    if not is_owner(e.sender_id):
        return await e.reply("🚫 You are not allowed to use this command.")

    IS_PUBLIC = not IS_PUBLIC
    save_mode(IS_PUBLIC)
    mode = "🌍 Public (All users allowed)" if IS_PUBLIC else "🔒 Private (Only OWNER/DEV)"
    await e.reply(f"✅ Mode changed successfully.\n\n**Current Mode:** {mode}")

########## BOT RUNNER ##########

LOGS.info("Bot has started.")
with bot:
    bot.run_until_disconnected()
    bot.loop.run_forever()
