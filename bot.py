import os, asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", "23422082"))
API_HASH = os.environ.get("API_HASH", "e9c7ad4dd0abf05990e8cfe409203620")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793802162:AAEVx-v86yVC4oyXFo8mqHzpa1U8-_tQxJA")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5338271513"))
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Savan:Savan@cluster0.p6n8k.mongodb.net/?retryWrites=true&w=majority")

bot = Client("savan_jod_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.get_database("auto_approve_db")
users_col = db.get_collection("users")

WELCOME_LINK = "https://t.me/+Pi6GvsfYlFUzZTg1"

async def add_user(user_id):
    await users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

# --- START COMMAND (Shows all commands) ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await add_user(message.from_user.id)
    caption = (
        f"👋 **Hey {message.from_user.first_name}!**\n\n"
        "🔥 **Welcome to Savan's Management Bot.**\n\n"
        "📜 **Available Commands:**\n"
        "🔹 `/approve` - Manual approval with counting (Admin Only)\n"
        "🔹 `/broadcast` - Send message to all users (Reply to a message)\n\n"
        f"📢 **Main Channel:** [JOIN NOW]({WELCOME_LINK})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ **Powered By: @Savan_Jod**"
    )
    await message.reply_text(caption, disable_web_page_preview=True)

# --- JOIN REQUEST HANDLER (Only Welcome Message) ---
@bot.on_chat_join_request()
async def welcome_req(client, message):
    user = message.from_user
    await add_user(user.id)
    welcome_text = (
        f"👋 **Hey {user.first_name}!**\n\n"
        "✅ Aapki join request humein mil gayi hai!\n"
        "Admin jald hi ise approve kar denge. ❤️\n\n"
        f"Tab tak hamara **Main Channel** join kar lo:\n👇👇👇\n"
        f"{WELCOME_LINK}\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await bot.send_message(user.id, welcome_text, disable_web_page_preview=True)
    except:
        pass

# --- MANUAL APPROVE WITH COUNTING ---
@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def manual_approve(client, message):
    chat_id = message.chat.id
    status_msg = await message.reply_text("🔄 **Processing requests... please wait.**")
    
    approved = 0
    failed = 0
    
    async for request in bot.get_chat_join_requests(chat_id):
        try:
            await bot.approve_chat_join_request(chat_id, request.from_user.id)
            approved += 1
            await asyncio.sleep(0.8) # Anti-flood delay
        except:
            failed += 1
            
    final_text = (
        "✅ **Approval Task Finished!**\n\n"
        f"📊 **Successfully Approved:** `{approved}`\n"
        f"❌ **Failed/Expired:** `{failed}`\n\n"
        "⚡ **System Status: Stable**\n"
        "⚡ **Owner: @Savan_Jod**"
    )
    await status_msg.edit(final_text)

# --- BROADCAST SYSTEM ---
@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Galti!**\nKisi message par reply karke `/broadcast` likho.")
    
    wait = await message.reply_text("🚀 **Broadcasting to all users...**")
    count = 0
    async for user in users_col.find():
        try:
            # Copy use karne se formatting (bold/italic/media) sahi rehti hai
            await message.reply_to_message.copy(user["user_id"])
            count += 1
            await asyncio.sleep(0.3)
        except: pass
    
    await wait.edit(f"✅ **Broadcast Completed!**\n\n📢 Total users reached: `{count}`")

if __name__ == "__main__":
    print("Savan Bhai, Bot is now Live with Broadcast!")
    bot.run()
    
