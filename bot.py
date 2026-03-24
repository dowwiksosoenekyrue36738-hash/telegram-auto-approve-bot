import os
import sys

# --- 🛠️ STEP 1: CRITICAL BYPASS FOR PYTHON 3.14 ---
# Ye lines Pyrogram ko crash hone se rokti hain
os.environ["PYROGRAM_COMPAT"] = "1"

import asyncio
import threading
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Bot (Py 3.14) Active! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# --- 🤖 BOT SETUP ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = AsyncIOMotorClient(MONGO_URI)["SavanDB"]["users"]

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        await db.update_one({"_id": request.from_user.id}, {"$set": {"name": request.from_user.first_name}}, upsert=True)
        await client.send_message(request.from_user.id, f"Hello {request.from_user.first_name}!\nApproved ✅\n\n⚡ By @SAVAN_JOD")
    except: pass

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
        # Naya event loop manually create karna padega 3.14 ke liye
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
