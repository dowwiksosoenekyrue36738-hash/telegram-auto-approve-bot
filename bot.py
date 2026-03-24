import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Professional Bot is Online! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- BOT CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- UI DESIGN ---
START_TEXT = """
**🚀 High-Speed Join Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests at maximum speed.

**Key Features:**
• ⚡ **Ultra-fast** bulk approval
• 🔄 **Concurrent processing**
• 📊 **Real-time** statistics
• 🛡️ **Rate limit** protection

**Owner:** @SAVAN_JOD
**Status:** `Running at Maximum Speed 🚀`
"""

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📊 Channel Stats", callback_data="stats"),
        InlineKeyboardButton("➕ Add to Channel", url=f"https://t.me/share/url?url=Admin+banayein+is+bot+ko")
    ],
    [InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")]
])

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(START_TEXT, reply_markup=START_BUTTONS)

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    except Exception as e:
        print(f"Join Error: {e}")

async def main():
    threading.Thread(target=run_web, daemon=True).start()
    try:
        await app.start()
        print("✅ SUCCESS: BOT IS CONNECTED!")
        await asyncio.Event().wait()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
