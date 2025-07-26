import os
import re
import logging
import asyncio
import uuid
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

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

LOGS = logging.getLogger("bot")
LOGS.setLevel(logging.INFO)

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

os.makedirs("downloads", exist_ok=True)
os.makedirs("encode", exist_ok=True)

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
    logs = getlogs()
    await e.reply(f"🧾 Logs:\n\n{logs[-4000:]}" if logs else "❌ No logs found.")

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

########## FILE + THUMB HANDLER ##########

@bot.on(events.NewMessage(incoming=True))
async def handle_upload(e):
    if e.photo:
        if is_owner(e.sender_id):
            os.system("rm thumb.jpg")
            await e.client.download_media(e.media, file="thumb.jpg")
            return await e.reply("**Thumbnail Saved Successfully.**")
        return

    if not e.video:
        return

    if not IS_PUBLIC and not is_owner(e.sender_id):
        return await e.reply("🚫 Bot is in private mode.")

    await e.reply("📥 Received video. Starting compression...")

    input_path = await e.download_media(file="downloads/")
    if not input_path:
        return await e.reply("❌ Failed to download the video.")

    # ✅ Rename with safe ASCII-only name
    safe_input = f"downloads/{uuid.uuid4().hex}.mp4"
    os.rename(input_path, safe_input)
    input_path = safe_input

    output_path = f"encode/{uuid.uuid4().hex}.mkv"

    # 🗜 FFmpeg compression
    cmd = f"""ffmpeg -i "{input_path}" -preset faster -c:v libx265 -s 1280x720 "{output_path}" -y"""
    process = await asyncio.create_subprocess_shell(cmd)
    await process.communicate()

    if not os.path.exists(output_path):
        return await e.reply("❌ Compression failed. Output file not found.")

    progress_msg = await e.reply("📤 Uploading... 0%")
    start_time = asyncio.get_event_loop().time()

    async def progress(current, total):
        percent = current * 100 / total
        try:
            await progress_msg.edit(f"📤 Uploading... {percent:.2f}%")
        except:
            pass

    await e.client.send_file(
        e.chat_id,
        output_path,
        force_document=True,
        thumb="thumb.jpg" if os.path.exists("thumb.jpg") else None,
        progress_callback=progress
    )

    os.remove(input_path)
    os.remove(output_path)

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
