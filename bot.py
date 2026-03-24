import os
import sys
import asyncio
import threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask

# --- 🛠 STEP 1: CRITICAL BYPASS ---
os.environ["PYROGRAM_COMPAT"] = "1"

import asyncio
import threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Savan Bot (Py 3.14) Active! 🚀"

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

# --- ✅ AUTO APPROVE LOGIC ---
@app.on_chat_join_request()
async def auto_approve(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    user_name = request.from_user.first_name

    try:
        # 1. Sabse pehle approve karo
        await client.approve_chat_join_request(chat_id, user_id)
        
        # 2. Database update karo (optional but good)
        await db.update_one({"id": user_id}, {"$set": {"name": user_name}}, upsert=True)
        
        # 3. Welcome message bhejo
        await client.send_message(user_id, f"Hello {user_name}! Your request to join has been approved ✅")
        
    except Exception as e:
        print(f"Error in auto_approve: {e}")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Savan Approval Bot is Active on 3.14! ⚡")

# --- 🚀 ASYNC ENTRY POINT ---
async def main():
    # Flask thread start karein
    threading.Thread(target=run_web, daemon=True).start()
    
    # Bot start karein
    async with app:
        print("✅ BOT STARTED SUCCESSFULLY ON PYTHON 3.14.3!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
        
