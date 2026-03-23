import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "")

bot = Client("savan_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DATABASE (With Bypass) ---
users_col = None
if MONGO_URI:
    try:
        mongo = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        users_col = mongo.get_database("bot_db").get_collection("users")
    except:
        print("DB Connection Failed - Running without DB")

LINK = "https://t.me/+Pi6GvsfYlFUzZTg1"

async def add_user(uid):
    if users_col is not None:
        try: await users_col.update_one({"id": uid}, {"$set": {"id": uid}}, upsert=True)
        except: pass

@bot.on_message(filters.command("start") & filters.private)
async def start(c, m):
    await add_user(m.from_user.id)
    await m.reply_text(f"👋 **Hey {m.from_user.first_name}!**\n\nBot is Live! 🚀\n\n/approve - Approve Req\n/broadcast - Message All\n\n📢 [Main Channel]({LINK})", disable_web_page_preview=True)

@bot.on_chat_join_request()
async def join(c, m):
    await add_user(m.from_user.id)
    try: await bot.send_message(m.from_user.id, f"👋 Welcome!\n\nJoin Channel:\n{LINK}")
    except: pass

@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def app(c, m):
    st = await m.reply_text("🔄 Processing...")
    ok, no = 0, 0
    async for r in bot.get_chat_join_requests(m.chat.id):
        try:
            await bot.approve_chat_join_request(m.chat.id, r.from_user.id)
            ok += 1
            await asyncio.sleep(1)
        except: no += 1
    await st.edit(f"✅ **Done!**\nApproved: {ok}\nFailed: {no}")

if __name__ == "__main__":
    print("Bot starting...")
    bot.run()
