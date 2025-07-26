import os
import psutil
from .worker import QUEUE, WORKING

async def sysinfo(event):
    """Returns basic system information."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    await event.reply(
        f"🖥️ <b>System Information</b>:\n\n"
        f"🔸 CPU Usage: <code>{cpu}%</code>\n"
        f"🔸 RAM Usage: <code>{ram}%</code>\n"
        f"🔸 Disk Usage: <code>{disk}%</code>",
        parse_mode="html"
    )

async def clearqueue(event):
    """Clears the queue and resets working flag."""
    QUEUE.clear()
    WORKING.clear()
    await event.reply("✅ Cleared the queue and reset working status.")

async def renew(event):
    """Deletes downloaded and encoded files to free up space."""
    os.system("rm -rf downloads/* encode/*")
    await event.reply("🧹 Cache cleared from `downloads/` and `encode/` folders.")
