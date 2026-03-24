import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask

# --- 🛠 COMPATIBILITY & CONFIG ---
os.environ["PYROGRAM_COMPAT"] = "1"

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_URL = os.environ.get("MONGO_URL", "")

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Bot is Active! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# --- 🤖 BOT CLIENT ---
app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- 📊 UI DESIGN ---
START_TEXT = """
**🚀 Savan High-Speed Join Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests at maximum speed.

**Key Features:**
• ⚡ **Ultra-fast** bulk approval
• 🔄 **Real-time** processing
• 📊 **Live** statistics
• 🛡️ **Rate limit** protection

**Owner:** @SAVAN_JOD
**Status:** `Running at Maximum Speed 🚀`
"""

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📊 Stats", callback_data="stats"),
        InlineKeyboardButton("➕ Add to Channel", url="https://t.me/share/url?url=Admin+banayein+is+bot+ko")
    ],
    [InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")]
])

# --- ✅ HANDLERS ---

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(START_TEXT, reply_markup=START_BUTTONS)

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        # Sabse pehle approve karo
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        # Confirmation message
        await client.send_message(request.from_user.id, f"**Welcome!** Aapki request accept ho gayi hai. ✅")
    except Exception as e:
        print(f"Approve Error: {e}")

# --- 🚀 EXECUTION ---

async def start_services():
    # 1. Flask ko background thread mein chalayein
    threading.Thread(target=run_web, daemon=True).start()
    
    # 2. Bot ko start karein
    print("Starting Savan Bot...")
    await app.start()
    print("✅ BOT IS LIVE!")
    
    # 3. Loop ko chalu rakhein
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        pass
        
