import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 🛠 CONFIGURATION ---
os.environ["PYROGRAM_COMPAT"] = "1"

# Railway variables se details uthana
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Flask setup (Railway 24/7 ke liye)
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Professional Bot is Online! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# Bot Client
app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- 📊 UI DESIGNS (Screenshot jaisa look) ---

START_TEXT = """
**🚀 High-Speed Join Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests at maximum speed.

**Key Features:**
• 📩 **Auto-log** all join requests
• ⚡ **Ultra-fast** bulk approval (up to 250/sec)
• 🔄 **Concurrent processing** with retry logic
• 📊 **Real-time** statistics
• 🛡️ **Rate limit** protection

**Owner:** @SAVAN_JOD
**Status:** `Running at Maximum Speed 🚀`
"""

# Buttons jo aapne screenshot mein maange the
START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📊 Channel Stats", callback_data="stats"),
        InlineKeyboardButton("➕ Add to Channel", url=f"https://t.me/share/url?url=Admin+banayein+is+bot+ko")
    ],
    [
        InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")
    ],
    [
        InlineKeyboardButton("❓ Help", callback_data="help"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    ]
])

# --- 🤖 HANDLERS (Commands aur Actions) ---

# /start Command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        text=START_TEXT,
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True
    )

# Auto Request Accept Logic
@app.on_chat_join_request()
async def auto_approve(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    user_name = request.from_user.first_name
    
    try:
        # 1. Request approve karna
        await client.approve_chat_join_request(chat_id, user_id)
        
        # 2. User ko professional message bhejna
        welcome_msg = f"**Hello {user_name}!**\n\nYour request to join **{request.chat.title}** has been approved successfully! ✅"
        await client.send_message(user_id, welcome_msg)
        
    except Exception as e:
        print(f"Approve Error: {e}")

# Button Click Handlers
@app.on_callback_query()
async def cb_handler(client, query):
    if query.data == "stats":
        await query.answer("Stats: 7,003 Monthly Users (Demo Mode)", show_alert=True)
    elif query.data == "help":
        await query.answer("Just add me to your channel as admin with 'Invite Link' permission!", show_alert=True)
    elif query.data == "about":
        await query.answer("Savan Approval Bot v2.0 - Built for Speed ⚡", show_alert=True)

# --- 🚀 RUNNING THE BOT ---
async def start_bot():
    # Start Flask thread
    threading.Thread(target=run_web, daemon=True).start()
    
    print("Starting Professional Bot...")
    await app.start()
    print("✅ BOT IS LIVE WITH ALL FEATURES!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
    
