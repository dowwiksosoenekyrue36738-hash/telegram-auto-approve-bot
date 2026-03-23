import os, asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIG
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "")

bot = Client("approve_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# DATABASE (Safe Mode)
users_col = None
if MONGO_URI:
    try:
        mongo = AsyncIOMotorClient(MONGO_URI)
        users_col = mongo.get_database("auto_approve_db").get_collection("users")
    except: pass

async def add_user(user_id):
    if users_col is not None:
        try: await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        except: pass

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await add_user(message.from_user.id)
    await message.reply_text("🤖 **Bot is Active!**\n\nOwner: @Savan_Jod")

@bot.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        await add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Welcome! Approved ✅")
    except: pass

if __name__ == "__main__":
    print("Bot is starting...")
    bot.run()
    
