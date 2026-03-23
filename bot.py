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

# --- DATABASE SETUP ---
users_col = None
if MONGO_URI:
    db_client = AsyncIOMotorClient(MONGO_URI)
    users_col = db_client["JoinBotDB"]["users"]

bot = Client("JoinRequestBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def add_user(user_id):
    if users_col is not None:
        await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await add_user(message.from_user.id)
    text = (
        "🤖 **Bot Commands**\n\n"
        "/start — Show commands\n"
        "/approve — Accept all pending requests\n"
        "/broadcast — Send message to all members\n"
        "/members — Show member stats\n\n"
        "Owner: @Savan_jod"
    )
    await message.reply_text(text)

@bot.on_chat_join_request()
async def auto_welcome(client, message):
    user = message.from_user
    await add_user(user.id)
    welcome_text = (
        f"Hey {user.first_name}! Welcome ❤️🫶🏼\n"
        "Aapki join request approve ho jyegi soon ✅\n"
        "Main channel join kar lo yaha:\n"
        "https://t.me/+Pi6GvsfYlFUzZTg1\n"
        "Updates miss mat karna! 🔥"
    )
    try: await bot.send_message(user.id, welcome_text)
    except: pass

@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def approve_all(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 Processing...")
    approved, failed = 0, 0
    try:
        async for request in bot.get_chat_join_requests(chat_id):
            try:
                await bot.approve_chat_join_request(chat_id, request.from_user.id)
                approved += 1
            except: failed += 1
        await msg.edit(f"✅ DONE ✓\n✔ Approved: {approved}\n❌ Failed: {failed}")
    except Exception as e: await msg.edit(f"❌ Error: {str(e)}")

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast.")
    msg = await message.reply_text("📡 Broadcasting...")
    done = 0
    if users_col is not None:
        async for user in users_col.find({}):
            try:
                await message.reply_to_message.copy(user["user_id"])
                done += 1
            except (UserIsBlocked, InputUserDeactivated):
                await users_col.delete_one({"user_id": user["user_id"]})
            except: continue
        await msg.edit(f"✅ Sent to: {done} members.")
    else: await msg.edit("❌ No Database Connected.")

@bot.on_message(filters.command("members") & filters.user(ADMIN_ID))
async def member_stats(client, message):
    if users_col is not None:
        count = await users_col.count_documents({})
        await message.reply_text(f"📊 Total Members: {count}")
    else: await message.reply_text("❌ No Database.")

# --- FIX FOR RENDER EVENT LOOP ERROR ---
async def main():
    await bot.start()
    print("Bot is Live!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
