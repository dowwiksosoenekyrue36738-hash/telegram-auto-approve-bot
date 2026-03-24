import os
import asyncio
import threading
from pyrogram import Client, filters
from flask import Flask

# --- 🌐 WEB SERVER (For Railway 24/7) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running! 🚀"

def run_web():
    # Railway automatically provides PORT
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- 🤖 BOT CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("SavanBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- ✅ HANDLERS ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Savan Bhai, Bot finally chal gaya! ✅")

@app.on_chat_join_request()
async def auto_approve(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
        await client.send_message(request.from_user.id, "Aapki request accept ho gayi hai! ✅")
    except Exception as e:
        print(f"Error: {e}")

# --- 🚀 START ---
if __name__ == "__main__":
    # Start Web Server in background
    threading.Thread(target=run_web, daemon=True).start()
    
    # Start Bot
    print("Bot starting...")
    app.run()
    
