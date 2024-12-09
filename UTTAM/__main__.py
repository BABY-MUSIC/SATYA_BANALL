import os
import logging
import threading
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from datetime import datetime
import pytz
from flask import Flask

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Config vars
API_ID = int(os.getenv("API_ID", "16457832"))
API_HASH = os.getenv("API_HASH", "3030874d0befdb5d05597deacc3e83ab")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7538146982:AAGeiAfuNVs-gEK1gfOHcPuwbv_5JCv2nvo")
LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID", "-1002043570167"))  # Log group ID
OWNER = os.getenv("OWNER", "BABY09_WORLD")

# Pyrogram client initialization
app = Client(
    "banall",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Flask app initialization
flask_app = Flask(__name__)

# Function to get current time in IST (Indian Standard Time)
def get_indian_time():
    tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_mention = message.from_user.mention  # Get the user's mention
    current_time = get_indian_time()
    user_id = message.from_user.id            # Get the user's ID
    user_username = message.from_user.username if message.from_user.username else "No Username"

    # Send a reply message to the user
    await message.reply_photo(
        photo="https://files.catbox.moe/3zu85t.jpg",
        caption=f"╭───────────────────⦿\n│❍ • ʜᴇʏ ᴛʜɪs ɪs ᴀ sɪᴍᴘʟᴇ ʙᴀɴ •\n│❍ • ᴀʟʟ ʙᴏᴛ ᴡʜɪᴄʜ ɪs ʙᴀsᴇᴅ ᴏɴ •\n│• ᴘʏʀᴏɢʀᴀᴍ •\n│❍ • ʟɪʙʀᴀʀʏ ᴛᴏ ʙᴀɴ ᴏʀ ᴅᴇsᴛʀᴏʏ •\n│❍ • ᴀʟʟ ᴛʜᴇ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴘ •\n│• ᴡɪᴛʜ ɪɴ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs •\n│❍ • ɴᴏ sᴛᴏᴘ + ɴᴏ ʟᴀɢ •\n├───────────────────⦿\n│❍ • ᴛʏᴘᴇ /ʙᴀɴᴀʟʟ ᴛᴏ ꜱᴇᴇ ᴍᴀɢɪᴄ ɪɴ │ • ɢʀᴏᴜᴘ •\n│❍ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➛ [ʙᴧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD) • \n╰───────────────────⦿",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("˹ ʙᴀʙʏ-ᴍᴜsɪᴄ ™˼𓅂│ᴜᴘᴅᴀᴛᴇ│", url=f"https://t.me/{OWNER}")
                ]       
            ]
        )
    )

    # Send a detailed log message to the logger group with user info
    await client.send_message(
        chat_id=LOGGER_GROUP_ID,
        text=f"```\n⋘ {current_time} ⋙```\n**【{client.me.mention} Lᴏɢɢᴇʀ :】**\n\n{user_mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ\n**➥ ᴜsᴇʀ_ɪᴅ:** {user_id}\n**➥ ᴜsᴇʀɴᴀᴍᴇ:** @{user_username}"
    )


@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("getting members from {}".format(message.chat.id))
    async for i in app.get_chat_members(message.chat.id):
        try:
            await app.ban_chat_member(chat_id=message.chat.id, user_id=i.user.id)
            print("kicked {} from {}".format(i.user.id, message.chat.id))
        except Exception as e:
            print("failed to kick {} from {}".format(i.user.id, e))           
    print("process completed")

# Send a startup log message to the logger group when the bot starts
async def send_startup_log(client):
    bot_mention = client.me.mention
    bot_id = client.me.id
    bot_username = client.me.username if client.me.username else "No Username"
    current_time = get_indian_time()  # Get the current time in IST

    # Send the startup log message to the logger group
    await client.send_message(
        chat_id=LOGGER_GROUP_ID,
        text=f"**【{bot_mention} sᴛᴀʀᴛᴇᴅ】**\n"
             f"⤥ɪᴅ: {bot_id}\n"
             f"⤥ᴜsᴇʀɴᴀᴍᴇ: {bot_username}\n"
             f"⤥ᴛɪᴍᴇ: {current_time}"
    )


# Flask route for testing
@flask_app.route('/')
def index():
    return "Flask web server is running!"

# Function to start Flask in a separate thread
def run_flask():
    flask_app.run(host='0.0.0.0', port=8000, threaded=True)

# Start the bot and Flask concurrently
if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start the Pyrogram client
    app.start()
    # Send the startup log message after the bot starts
    app.loop.run_until_complete(send_startup_log(app)) 
    logging.info("Banall-Bot Booted Successfully")

    # Keep the bot running with idle
    idle()
