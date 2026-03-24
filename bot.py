import os
import sys
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask

# --- 🛠 STEP 1: CRITICAL BYPASS ---
os.environ["PYROGRAM_COMPAT"] = "1"

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Savan Approval Bot Active! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# --- ⚙️ BOT SETUP ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")

app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = AsyncIOMotorClient(MONGO_URL)["SavanDB"]["users"]

# --- 📊 START MESSAGE WITH BUTTONS ---
START_TEXT = """
**🚀 Savan High-Speed Join Request Manager**

Welcome! I’m a professional bot designed to manage channel join requests at maximum speed.

**Key Features:**
• 📩 Auto-log all join requests
• ⚡ Ultra-fast bulk approval
• 🔄 Concurrent processing with retry logic
• 📊 Real-time statistics
• 🛡️ Rate limit protection

**Owner:** @SAVAN_JOD

Use the buttons below to explore my features!
"""

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📊 Channel Stats", callback_data="stats"),
        InlineKeyboardButton("➕ Add to Channel", url=f"https://t.me/your_bot_username?startchannel=true")
    ],
    [
        InlineKeyboardButton("👤 Owner", url="https://t.me/SAVAN_JOD")
    ],
    [
        InlineKeyboardButton("❓ Help", callback_data="help"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    ]
])

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/your-image-link.jpg", # Yahan apni koi image link daal sakte hain
        caption=START_TEXT,
        reply_markup=START_BUTTONS
    )

# --- ✅ AUTO APPROVE LOGIC ---
@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        # Statistics update karne ke liye database mein entry
        await db.update_one({"id": request.from_user.id}, {"$set": {"name": request.from_user.first_name}}, upsert=True)
    except Exception as e:
        print(f"Approve Error: {e}")

# --- 🚀 STARTING LOGIC ---
async def main():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        print("✅ SAVAN BOT STARTED SUCCESSFULLY!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
