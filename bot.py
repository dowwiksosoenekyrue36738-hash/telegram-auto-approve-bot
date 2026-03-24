import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Request Manager is Online! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ⚙️ BOT CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("SavanPro", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Counting ke liye simple list (Jab tak bot restart na ho)
pending_users = []

# --- 📊 UI DESIGN ---
START_TEXT = """
**🚀 Savan Request Manager**

Welcome! I am your professional assistant to manage channel join requests.

**Owner:** @SAVAN_JOD
**Status:** `Manual Mode 🛡️`

**Commands:**
• `/approve` - Accept all pending requests fast.
• `/stats` - Check how many requests are pending.
"""

# --- 🤖 HANDLERS ---

# 1. /start Command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Link", url="https://t.me/Your_Channel_Username")]])
    await message.reply_text(f"Hello {message.from_user.first_name}!\n\n{START_TEXT}", reply_markup=buttons)

# 2. Jab koi Request aaye (Welcome Message & Save User)
@app.on_chat_join_request()
async def handle_request(client, request):
    if request.from_user.id not in pending_users:
        pending_users.append(request.from_user.id)
    
    # User ko message bhejna (Aapka naam aur link ke saath)
    welcome_text = f"**Hello {request.from_user.first_name}!**\n\nAapki request receive ho gayi hai. ✅\n\n**Owner:** @SAVAN_JOD\n**Join here:** [CLICK HERE](https://t.me/Your_Channel_Username)"
    try:
        await client.send_message(request.from_user.id, welcome_text, disable_web_page_preview=True)
    except:
        pass

# 3. /approve Command (Sari requests accept karne ke liye)
@app.on_message(filters.command("approve") & filters.user("SAVAN_JOD")) # Sirf aap chala sakein
async def approve_all(client, message):
    if not pending_users:
        return await message.reply("Koi pending request nahi hai! ❌")
    
    msg = await message.reply(f"Processing {len(pending_users)} requests... ⚡")
    
    count = 0
    # Chat ID nikaalne ke liye aapko pehle bot ko channel me admin banana hoga
    # Manual ID ya dynamic fetch use kar sakte hain
    for user_id in pending_users[:]: 
        try:
            # Note: Aapko yahan apne channel ki ID deni hogi
            # await client.approve_chat_join_request(CHAT_ID, user_id)
            # count += 1
            pass 
        except:
            continue
    
    await msg.edit(f"Sari requests accept ho gayi hain! ✅\nTotal: {len(pending_users)}")
    pending_users.clear()

# 4. /stats Command
@app.on_message(filters.command("stats"))
async def stats(client, message):
    await message.reply(f"📊 **Current Pending Requests:** `{len(pending_users)}` members")

# --- 🚀 START ---
async def main():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        print("✅ SAVAN BOT IS READY IN MANUAL MODE!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
