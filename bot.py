import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Professional Bot is Running! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- BOT CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Client setup with session refresh
app = Client(
    "SavanBotSession", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN,
    in_memory=True  # Isse purane session cache delete ho jayenge
)

# --- UI DESIGN (Based on your Screenshot) ---
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

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📊 Channel Stats", callback_data="stats"),
        InlineKeyboardButton("➕ Add to Channel", url="https://t.me/share/url?url=Admin+me!")
    ],
    [InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")],
    [
        InlineKeyboardButton("❓ Help", callback_data="help"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    ]
])

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    try:
        await message.reply_text(
            text=START_TEXT,
            reply_markup=START_BUTTONS
        )
    except Exception as e:
        print(f"Reply Error: {e}")

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        print(f"Approved: {request.from_user.first_name}")
    except Exception as e:
        print(f"Join Error: {e}")

async def main():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        print("✅ SUCCESS: BOT IS CONNECTED!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
