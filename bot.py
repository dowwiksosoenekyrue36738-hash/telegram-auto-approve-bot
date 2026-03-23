import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIG
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Savan:Savan@cluster0.p6n8k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

bot = Client("approve_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
users_col = AsyncIOMotorClient(MONGO_URI).get_database("auto_approve_db").get_collection("users")

async def add_user(user_id):
    await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await add_user(message.from_user.id)
    await message.reply_text("🤖 **Bot is Active!**")

@bot.on_chat_join_request()
async def auto_approve(client, message):
    try:
        await client.approve_chat_join_request(message.chat.id, message.from_user.id)
        await add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Hey! Your request is approved. ✅")
    except:
        pass

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message!")
    async for user in users_col.find():
        try:
            await message.reply_to_message.copy(user["user_id"])
            await asyncio.sleep(0.1)
        except:
            pass
    await message.reply_text("✅ Done!")

if __name__ == "__main__":
    bot.run()
    
