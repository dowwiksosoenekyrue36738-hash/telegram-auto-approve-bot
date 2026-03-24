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
# Variables ko check karne ke liye print statement daala hai
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "SavanBot",
    api_id=int(API_ID) if API_ID else 0,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- UI DESIGN (Screenshot Jaisa) ---
START_TEXT = """
**🚀 Savan High-Speed Join Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests at maximum speed.

**Owner:** @SAVAN_JOD
**Status:** `Active ✅`
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📊 Stats", callback_data="stats"),
     InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")]
])

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(START_TEXT, reply_markup=START_BUTTONS)

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        await client.send_message(request.from_user.id, "Approved! ✅")
    except Exception as e:
        print(f"Join Error: {e}")

async def main():
    threading.Thread(target=run_web, daemon=True).start()
    try:
        print("Bot is connecting to Telegram...")
        await app.start()
        print("✅ SUCCESS: BOT IS CONNECTED TO TELEGRAM!")
        await asyncio.Event().wait()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
