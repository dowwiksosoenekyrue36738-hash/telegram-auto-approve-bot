import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
import threading

# Web server for Railway
app = Flask(__name__)
@app.url_map.add
@app.route('/')
def hello(): return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Bot Logic
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Savan Bhai, Bot chal gaya! ✅")

@bot.on_chat_join_request()
async def join(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    bot.run()
    
