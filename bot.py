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
# Replace with your actual Telegram ID (Get it from @MissRose_bot using /id)
OWNER_ID = int(os.environ.get("OWNER_ID", 5727181512)) 

app = Client("SavanUltimate", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Temporary storage
pending_db = {} 
USERS_FILE = "users.txt"

# Save user for broadcast
def add_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: pass
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

# --- 🤖 HANDLERS ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    add_user(message.from_user.id)
    text = (
        f"**Hello {message.from_user.first_name}!**\n\n"
        "Welcome to **Savan Request Manager**.\n\n"
        "**Commands:**\n"
        "• `/approve` - Fast accept all pending requests\n"
        "• `/stats` - Check pending members count\n"
        "• `/broadcast` - Send message to all (Reply to a msg)\n\n"
        "**Owner:** @SAVAN_JOD"
    )
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Channel Link", url="https://t.me/Your_Channel_Link")]])
    await message.reply_text(text, reply_markup=buttons)

@app.on_chat_join_request()
async def handle_request(client, request):
    chat_id = request.chat.id
    user_id = request.from_user.id
    add_user(user_id)
    
    if chat_id not in pending_db: pending_db[chat_id] = []
    if user_id not in pending_db[chat_id]: pending_db[chat_id].append(user_id)
    
    try:
        await client.send_message(
            user_id, 
            "**Hello! Aapki request receive ho gayi hai. ✅**\n\nOwner: @SAVAN_JOD"
        )
    except: pass

@app.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_all(client, message):
    if not pending_db:
        return await message.reply("Koi pending request nahi hai! ❌")
    
    status = await message.reply("🚀 **Processing all requests... Please wait.**")
    approved_count = 0
    
    for chat_id in list(pending_db.keys()):
        for user_id in pending_db[chat_id][:]:
            try:
                await client.approve_chat_join_request(chat_id, user_id)
                approved_count += 1
                pending_db[chat_id].remove(user_id)
            except: continue
    
    await status.edit(f"✅ **Done!** Total `{approved_count}` members approved.")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("Please reply to a message to broadcast it! 📢")
    
    if not os.path.exists(USERS_FILE):
        return await message.reply("No users found in database.")

    exmsg = await message.reply("🚀 **Broadcast started...**")
    with open(USERS_FILE, "r") as f:
        ids = f.read().splitlines()

    done = 0
    failed = 0
    for user_id in ids:
        try:
            await message.reply_to_message.copy(int(user_id))
            done += 1
            await asyncio.sleep(0.1) # Avoid spam limits
        except:
            failed += 1
            continue
            
    await exmsg.edit(f"📢 **Broadcast Completed!**\n\n✅ Sent: `{done}`\n❌ Failed: `{failed}`")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    total_pending = sum(len(u) for u in pending_db.values())
    db_users = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            db_users = len(f.read().splitlines())
    await message.reply(f"📊 **Bot Stats**\n\n• Pending Requests: `{total_pending}`\n• Database Users: `{db_users}`")

# --- 🚀 RUN ---
async def main():
    threading.Thread(target=run_web, daemon=True).start()
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
