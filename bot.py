import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIG
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Savan:Savan@cluster0.p6n8k.mongodb.net/?retryWrites=true&w=majority")

bot = Client("savan_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = AsyncIOMotorClient(MONGO_URI).get_database("db")
users_col = db.get_collection("users")
LINK = "https://t.me/+Pi6GvsfYlFUzZTg1"

async def add_user(uid):
    await users_col.update_one({"id": uid}, {"$set": {"id": uid}}, upsert=True)

@bot.on_message(filters.command("start") & filters.private)
async def start(c, m):
    await add_user(m.from_user.id)
    txt = f"👋 Hey {m.from_user.first_name}!\n\n/approve - Approve Req\n/broadcast - Message All\n\n📢 [Main Channel]({LINK})"
    await m.reply_text(txt, disable_web_page_preview=True)

@bot.on_chat_join_request()
async def join(c, m):
    uid = m.from_user.id
    await add_user(uid)
    try:
        await bot.send_message(uid, f"👋 Welcome!\n\nJoin Main Channel:\n{LINK}")
    except:
        pass

@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def app(c, m):
    status = await m.reply_text("🔄 Processing...")
    ok, no = 0, 0
    async for r in bot.get_chat_join_requests(m.chat.id):
        try:
            await bot.approve_chat_join_request(m.chat.id, r.from_user.id)
            ok += 1
            await asyncio.sleep(1)
        except:
            no += 1
    await status.edit(f"✅ Approved: {ok}\n❌ Failed: {no}")

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def bc(c, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to a message!")
    status = await m.reply_text("🚀 Sending...")
    cnt = 0
    async for u in users_col.find():
        try:
            await m.reply_to_message.copy(u["id"])
            cnt += 1
            await asyncio.sleep(0.3)
        except:
            pass
    await status.edit(f"✅ Sent to {cnt} users.")

if __name__ == "__main__":
    bot.run()
    
