import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIG (Variables Railway se uthayega) ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
MONGO_URI = os.environ.get("MONGO_URI", "")

# --- CLIENTS ---
bot = Client("savan_jod", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = AsyncIOMotorClient(MONGO_URI).get_database("bot_db")
users_col = db.get_collection("users")

LINK = "https://t.me/+Pi6GvsfYlFUzZTg1"

# --- HELPER ---
async def add_user(uid):
    await users_col.update_one({"id": uid}, {"$set": {"id": uid}}, upsert=True)

# --- COMMANDS ---
@bot.on_message(filters.command("start") & filters.private)
async def start(c, m):
    await add_user(m.from_user.id)
    text = (
        f"👋 **Hey {m.from_user.first_name}!**\n\n"
        "Welcome to Savan's Management Bot.\n\n"
        "📜 **Commands:**\n"
        "🔹 `/approve` - Approve Pending Requests\n"
        "🔹 `/broadcast` - Send Message to All\n\n"
        f"📢 [Main Channel]({LINK})"
    )
    await m.reply_text(text, disable_web_page_preview=True)

@bot.on_chat_join_request()
async def join_req(c, m):
    uid = m.from_user.id
    await add_user(uid)
    try:
        await bot.send_message(uid, f"👋 **Welcome!**\n\nAapki request mil gayi hai.\n\n📢 **Join Channel:** {LINK}")
    except: pass

@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def approve(c, m):
    status = await m.reply_text("🔄 **Processing...**")
    ok, no = 0, 0
    async for r in bot.get_chat_join_requests(m.chat.id):
        try:
            await bot.approve_chat_join_request(m.chat.id, r.from_user.id)
            ok += 1
            await asyncio.sleep(1)
        except: no += 1
    await status.edit(f"✅ **Done!**\n\nApproved: `{ok}`\nFailed: `{no}`")

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(c, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to a message to broadcast!")
    status = await m.reply_text("🚀 **Sending...**")
    count = 0
    async for u in users_col.find():
        try:
            await m.reply_to_message.copy(u["id"])
            count += 1
            await asyncio.sleep(0.3)
        except: pass
    await status.edit(f"✅ **Broadcast Done!**\nSent to `{count}` users.")

if __name__ == "__main__":
    bot.run()
    
