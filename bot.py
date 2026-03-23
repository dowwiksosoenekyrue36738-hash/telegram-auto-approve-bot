import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIGURATION
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Savan:Savan@cluster0.p6n8k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# CLIENTS
bot = Client("auto_approve_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.get_database("auto_approve_db")
users_col = db.get_collection("users")

# FUNCTIONS
async def add_user(user_id):
    if users_col is not None:
        await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

# HANDLERS
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await add_user(message.from_user.id)
    await message.reply_text("🤖 **Bot is Active!**\n\nOwner: @Savan_Jod")

@bot.on_chat_join_request()
async def auto_welcome(client, message):
    user = message.from_user
    chat = message.chat
    try:
        await client.approve_chat_join_request(chat.id, user.id)
        await add_user(user.id)
        welcome_text = (
            f"Hey {user.first_name}! Welcome ❤️\n"
            "Aapki join request approve ho gayi hai ✅\n"
            "Updates ke liye channel join rakhein!"
        )
        try:
            await bot.send_message(user.id, welcome_text)
        except:
            pass
    except Exception as e:
        print(f"Approval Error: {e}")

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast!")
    msg = await message.reply_text("🚀 Broadcasting...")
    done = 0
    async for user in users_col.find():
        try:
            await message.reply_to_message.copy(user["user_id"])
            done += 1
            await asyncio.sleep(0.1)
        except:
            pass
    await msg.edit(f"✅ Broadcast Complete!\nSent to: {done} users.")

if __name__ == "__main__":
    bot.run()
    
