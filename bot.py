import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 🌐 WEB SERVER (Railway keep-alive) ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Ultimate is Running! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ⚙️ CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("SavanUltimate", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Pending requests store karne ke liye
pending_db = {} 

# --- 🤖 HANDLERS ---

# 1. /start Command (Professional Look)
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    text = (
        f"**Hello {message.from_user.first_name}!**\n\n"
        "Welcome to **Savan Request Manager**. I will help you manage your channel requests manually.\n\n"
        "**Commands:**\n"
        "• `/approve` - Fast accept all pending requests\n"
        "• `/stats` - Check pending members count\n\n"
        "**Owner:** @SAVAN_JOD"
    )
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Link", url="https://t.me/Your_Channel_Link")]])
    await message.reply_text(text, reply_markup=buttons)

# 2. Jab Request Aaye (No Auto-Approve, Just Logging & Welcome)
@app.on_chat_join_request()
async def handle_request(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    
    # Store request
    if chat_id not in pending_db: pending_db[chat_id] = []
    if user_id not in pending_db[chat_id]: pending_db[chat_id].append(user_id)
    
    # User ko Welcome message (With your username)
    welcome_text = (
        f"**Hello {request.from_user.first_name}!**\n\n"
        "Aapki request receive ho gayi hai. ✅\n\n"
        "**Owner:** @SAVAN_JOD\n"
        "**Join here:** [CLICK HERE](https://t.me/Your_Channel_Link)"
    )
    try:
        await client.send_message(user_id, welcome_text, disable_web_page_preview=True)
    except:
        pass

# 3. /approve Command (Sari request accept karne ke liye)
@app.on_message(filters.command("approve"))
async def approve_all(client, message):
    if not pending_db:
        return await message.reply("Koi pending request nahi hai! ❌")
    
    status = await message.reply("🚀 **Processing all requests... Please wait.**")
    approved_count = 0
    
    for chat_id in list(pending_db.keys()):
        for user_id in pending_db[chat_id][:]:
            try:
                await client.approve_chat_join_request(chat_id, user_id)
                approved_count += 1
                pending_db[chat_id].remove(user_id)
            except:
                continue
    
    await status.edit(f"✅ **Done!**\n\nTotal `{approved_count}` members approved by @SAVAN_JOD.")

# 4. /stats Command (Counting)
@app.on_message(filters.command("stats"))
async def stats(client, message):
    total = sum(len(u) for u in pending_db.values())
    await message.reply(f"📊 **Current Pending Requests:** `{total}` members")

# --- 🚀 RUN ---
async def main():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
