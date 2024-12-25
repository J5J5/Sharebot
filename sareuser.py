from pyrogram import Client, filters
from flask import Flask, render_template
import asyncio
import random

# Initialize the bot client
app = Client("my_bot", api_id=9212418, api_hash="d783f8ce3d816448d29c4cc2258f838a")

# Flask web app for serving HTML
web_app = Flask(__name__)

# List to hold groups
forwarding_groups = ["ssssiiiiil", "ff2zz1"]
is_forwarding_enabled = False

# Pyrogram bot routes
@app.on_message(filters.command("add") & filters.private)
async def add_group(client, message):
    group_username = message.command[1] if len(message.command) > 1 else None
    if group_username:
        forwarding_groups.append(group_username)
        await message.reply(f"✅ Group '{group_username}' has been successfully added to the forwarding list.")
    else:
        await message.reply("❌ Please provide a valid group username to add.")

@app.on_message(filters.command("rem") & filters.private)
async def remove_group(client, message):
    group_username = message.command[1] if len(message.command) > 1 else None
    if group_username in forwarding_groups:
        forwarding_groups.remove(group_username)
        await message.reply(f"✅ Group '{group_username}' has been successfully removed from the forwarding list.")
    else:
        await message.reply("❌ The specified group was not found in the forwarding list.")

@app.on_message(filters.command("toggle") & filters.private)
async def toggle_forwarding(client, message):
    global is_forwarding_enabled
    is_forwarding_enabled = not is_forwarding_enabled
    status = "enabled" if is_forwarding_enabled else "disabled"
    await message.reply(f"🔄 Forwarding has been {status}.")

async def forward_random_messages():
    while True:
        if is_forwarding_enabled:
            for group_username in forwarding_groups:
                messages = []
                async for message in app.get_chat_history(group_username, limit=100):
                    if message.from_user:
                        messages.append(message)
                if messages:
                    message_to_forward = random.choice(messages)
                    target_channel = "qa8tm"
                    if message_to_forward.text and not any(char.isdigit() for char in message_to_forward.text):
                        await app.send_message(chat_id=target_channel, text=message_to_forward.text)
                    elif message_to_forward.voice:
                        await app.send_voice(chat_id=target_channel, voice=message_to_forward.voice.file_id)
                    elif message_to_forward.audio:
                        await app.send_audio(chat_id=target_channel, audio=message_to_forward.audio.file_id)
        await asyncio.sleep(14400)

@app.on_message(filters.command("start"))
async def start(client, message):
    """Start the forwarding task."""
    app.loop.create_task(forward_random_messages())

@app.on_message(filters.command("help"))
async def help(client, message):
    await message.reply("""
/add username - to add group 
/rem username - to remove group
/toggle - to start the share
/start - to start the task""")

# Flask routes
@web_app.route("/")
def index():
    return "HTML Deployment is Live! Bot is running in the background."

# Run Flask and Pyrogram together
def run_both():
    loop = asyncio.get_event_loop()
    loop.create_task(app.start())
    web_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run_both()
