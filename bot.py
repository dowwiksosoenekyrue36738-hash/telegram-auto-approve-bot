import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Ultimate Bot is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ⚙️ BOT CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("SavanUltimate", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Pending users ki list (Counting ke liye)
pending_requests = {}

# --- 📊 UI DESIGNS ---
START_TEXT = """
**🚀 Savan High-Speed Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests manually with maximum speed.

**Commands:**
• `/approve` - Bulk approve all pending requests ⚡
• `/stats` - Check pending members count 📊

**Status:** `Manual Mode - Waiting for Command 🛡️`
"""

# --- 🤖 HANDLERS ---

# 1. /start Command (With your Name & Link)
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channel Link", url="https://t.me/Your_Channel_Link")],
        [InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")]
    ])
    await message.reply_text(
        f"**Hello {message.from_user.first_name}!**\n\n{START_TEXT}\n\n**Owner:** @SAVAN_JOD", 
        reply_markup=buttons
    )

# 2. Join Request Handler (No Auto-Approve, Just Logging & Welcome)
@app.on_chat_join_request()
async def handle_join(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    
    # Store request for manual approval
    if chat_id not in pending_requests:
        pending_requests[chat_id] = []
    if user_id not in pending_requests[chat_id]:
        pending_requests[chat_id].append(user_id)

    # Welcome message user ko (With your username & link)
    welcome_msg = (
        f"**Hello {request.from_user.first_name}!**\n\n"
        f"Aapki request receive ho gayi hai. ✅\n\n"
        f"**Owner:** @SAVAN_JOD\n"
        f"**Channel:** [Join Here](https://t.me/Your_Channel_Link)"
    )
    try:
        await client.send_message(user_id, welcome_msg, disable_web_page_preview=True)
    except:
        pass

# 3. /approve Command (Fast Bulk Approval)
@app.on_message(filters.command("approve"))
async def bulk_approve(client, message):
    if not pending_requests:
        return await message.reply("No pending requests found! ❌")
    
    status_msg = await message.reply("🚀 **Processing all requests at maximum speed...**")
    total_approved = 0

    for chat_id in list(pending_requests.keys()):
        for user_id in pending_requests[chat_id][:]:
            try:
                await client.approve_chat_join_request(chat_id, user_id)
                total_approved += 1
                pending_requests[chat_id].remove(user_id)
                # Anti-flood delay for safety
                if total_approved % 50 == 0:
                    await asyncio.sleep(1)
            except:
                continue
    
    await status_msg.edit(f"✅ **Success!**\n\nTotal Members Approved: `{total_approved}`\nProcessed by: @SAVAN_JOD")

# 4. /stats Command (Counting)
@app.on_message(filters.command("stats"))
async def show_stats(client, message):
    count = sum(len(users) for users in pending_requests.values())
    await message.reply(f"📊 **Current Stats:**\n\nPending Requests: `{count}`\nManager: @SAVAN_JOD")

# --- 🚀 EXECUTION ---
async def start_services():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        print("✅ SUCCESS: SAVAN ULTIMATE BOT IS READY!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_services())
    
