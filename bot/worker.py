from .FastTelethon import download_file, upload_file
import logging
from .funcn import *
from .config import *
from telethon.tl.custom import Button
import os
from pathlib import Path
import time
import asyncio

LOGS = logging.getLogger("worker")
QUEUE = {}
WORKING = []


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        processing_file_name = dl.replace(f"downloads/", "").replace(f"_", " ")
        ans = f"Processing Media:\n{processing_file_name}\n\nDownloaded:\n{ov}\n\nCompressed:\n{ot}"
        await e.answer(ans, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        await e.answer("Someting Went Wrong.\nSend Media Again.", cache_time=0, alert=True)


async def dl_link(event):
    if not event.is_private:
        return
    if not is_authorized(event.sender_id):
        return await event.reply("**Sorry You're not An Authorised User!**")

    link, name = "", ""
    try:
        link = event.text.split()[1]
        name = event.text.split()[2]
    except BaseException:
        pass
    if not link:
        return
    if WORKING or QUEUE:
        QUEUE.update({link: name})
        return await event.reply(f"** Added {link} in QUEUE**")

    WORKING.append(1)
    s = dt.now()
    xxx = await event.reply("** Downloading...**")
    try:
        dl = await fast_download(xxx, link, name)
    except Exception as er:
        WORKING.clear()
        LOGS.info(er)
        return
    es = dt.now()
    kk = dl.split("/")[-1]
    aa = kk.split(".")[-1]
    newFile = dl.replace(f"downloads/", "").replace(f"_", " ")
    rr = "encode"
    bb = kk.replace(f".{aa}", ".mkv")
    out = f"{rr}/{bb}"
    thum = "thumb.jpg"
    dtime = ts(int((es - s).seconds) * 1000)
    hehe = f"{out};{dl};0"
    wah = code(hehe)
    nn = await xxx.edit(
        "**🗜 Compressing...**",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL", data=f"skip{wah}")],
        ],
    )
    cmd = f"""ffmpeg -i "{dl}" {ffmpegcode[0]} "{out}" -y"""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await xxx.edit(str(er) + "\n\n**ERROR**")
            WORKING.clear()
            os.remove(dl)
            return os.remove(out)
    except BaseException:
        pass
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await xxx.client.send_message(xxx.chat_id, "** Uploading...**")
    with open(out, "rb") as f:
        ok = await upload_file(
            client=xxx.client,
            file=f,
            name=out,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "** Uploading...**")
            ),
        )
    await nnn.delete()
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    a1 = await info(dl, xxx)
    a2 = await info(out, xxx)
    dk = f"<b>File Name:</b> {newFile}\n\n<b>Original File Size:</b> {hbs(org)}\n<b>Encoded File Size:</b> {hbs(com)}\n<b>Encoded Percentage:</b> {per}\n\n<b>Get Mediainfo Here:</b> <a href='{a1}'>Before</a>/<a href='{a2}'>After</a>\n\n<i>Downloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}</i>"
    ds = await e.client.send_file(
        e.chat_id, file=ok, force_document=True, caption=dk, link_preview=False, thumb=thum, parse_mode="html"
    )
    os.remove(dl)
    os.remove(out)
    WORKING.clear()


async def encod(event):
    # Your existing encod() remains unchanged
    ...


# ✅ Add this at the bottom to handle CANCEL button
async def skip(event):
    try:
        data = event.data.decode("utf-8")
        if "skip" in data:
            parts = data.replace("skip", "").split(";")
            if len(parts) >= 2:
                file_path = parts[1]
                if os.path.exists(file_path):
                    os.remove(file_path)
            WORKING.clear()
            await event.answer("⛔️ Cancelled!", alert=True)
            await event.edit("**Encoding Cancelled.**")
    except Exception as er:
        LOGS.info(f"Error during cancel: {er}")
        await event.answer("❌ Failed to cancel.", alert=True)
