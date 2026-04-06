import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 🌐 WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Savan Ultimate is Running! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ⚙️ CONFIG ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0)) # Add your Telegram ID here

app = Client("SavanUltimate", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Data Stores
pending_db = {} 
USERS_FILE = "users.txt"

# Helper to save users for broadcast
def add_user(user_id):
    if not os.path.exists(USERS_FILE): open(USERS_FILE, "a").close()
    with open(USERS_FILE, "r+") as f:
        lines = f.read().splitlines()
        if str(user_id) not in lines:
            f.write(f"{user_id}\n")

# --- 🤖 HANDLERS ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    add_user(message.from_user.id) # Save user for broadcast
    text = (
        f"**Hello {message.from_user.first_name}!**\n\n"
        "Welcome to **Savan Request Manager**.\n\n"
        "**Commands:**\n"
        "• `/approve` - Accept all requests\n"
        "• `/stats` - Check pending count\n"
        "• `/broadcast` - (Owner Only) Send message to all users\n\n"
        "**Owner:** @SAVAN_JOD"
    )
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Link", url="https://t.me/Your_Channel_Link")]])
    await message.reply_text(text, reply_markup=buttons)

@app.on_chat_join_request()
async def handle_request(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    add_user(user_id) # Save even those who just requested
    
    if chat_id not in pending_db: pending_db[chat_id] = []
    if user_id not in pending_db[chat_id]: pending_db[chat_id].append(user_id)
    
    welcome_text = f"**Hello {request.from_user.first_name}!**\nAapki request receive ho gayi hai. ✅"
    try:
        await client.send_message(user_id, welcome_text)
    except:
        pass

# --- 📢 BROADCAST FEATURE ---
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply_text("**Usage:** Reply to a message with `/broadcast` to send it to everyone.")
    
    if not os.path.exists(USERS_FILE):
        return await message.reply_text("No users found to broadcast.")

    with open(USERS_FILE, "r") as f:
        user_ids = f.read().splitlines()

    sent = 0
    failed = 0
    msg = await message.reply_text(f"🚀 **Broadcast Started...** Sending to {len(user_ids)} users.")

    for user_id in user_ids:
        try:
            await message.reply_to_message.copy(int(user_id))
            sent += 1
            await asyncio.sleep(0.1) # Flood prevention
        except:
            failed += 1
    
    await msg.edit(f"✅ **Broadcast Complete!**\n\n👤 Total Users: `{len(user_ids)}` \n📤 Sent: `{sent}`\n🚫 Failed: `{failed}`")

@app.on_message(filters.command("approve"))
async def approve_all(client, message):
    if not pending_db:
        return await message.reply("Koi pending request
                                   
