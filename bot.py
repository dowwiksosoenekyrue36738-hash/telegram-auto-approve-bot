import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserIsBlocked, InputUserDeactivated
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
MONGO_URI = os.environ.get("MONGO_URI", "") 

# Initialize Client without starting it globally
bot = Client("JoinRequestBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database Setup
users_col = None
if MONGO_URI:
    db_client = AsyncIOMotorClient(MONGO_URI)
    users_col = db_client["JoinBotDB"]["users"]

async def add_user(user_id):
    if users_col is not None:
        await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await add_user(message.from_user.id)
    await message.reply_text("🤖 Bot is Active!\nOwner: @Savan_jod")

@bot.on_chat_join_request()
async def auto_welcome(client, message):
   user = message.from_user
    await add_user(user.id)
    welcome_text = (
        f"Hey {user.first_name}! Welcome ❤️\n"
        "Aapki join request approve ho jayegi soon ✅\n"
        "Main channel join kar lo yaha:\n"
        "https://t.me/+Pi6GvsfYlFUzZTg1\n"
        "Updates miss mat karna! 🔥"
    )
    try:
        await bot.send_message(user.id, welcome_text)
    except:
        pass
        
@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def approve_all(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 Processing...")
    approved = 0
    async for request in bot.get_chat_join_requests(chat_id):
        try:
            await bot.approve_chat_join_request(chat_id, request.from_user.id)
            approved += 1
        except: pass
    await msg.edit(f"✅ Approved: {approved}\nRG - @Savan_jod")

# --- MAIN RUNNER (Fix for Render Error) ---
async def main():
    async with bot:
        print("Bot is Live on Render!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
