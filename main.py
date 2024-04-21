import asyncio
import os
import time
from uuid import uuid4

from telethon import TelegramClient, events
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.types import Message, UpdateNewMessage

from cansend import CanSend
from config import *
from terabox import get_data
from tools import (
    convert_seconds,
    download_file,
    download_image_to_bytesio,
    extract_code_from_url,
    get_formatted_size,
    get_urls_from_string,
    is_user_on_chat,
)

bot = TelegramClient("tele", API_ID, API_HASH)

@bot.on(
    events.NewMessage(
        pattern="/start$",
        incoming=True,
        outgoing=False,
        func=lambda x: x.is_private,
    )
)
async def start(m: UpdateNewMessage):
    reply_text = f"""
Hello! I am a bot to download videos from terabox.
Send me the terabox link and I will start downloading it.
Join @RoldexVerse For Updates
[Source Code](https://github.com/r0ld3x/terabox-downloader-bot) """
    check_if = await is_user_on_chat(bot, "@RoldexVerse", m.peer_id)
    if not check_if:
        return await m.reply("Please join @RoldexVerse then send me the link again.")
    check_if = await is_user_on_chat(bot, "@RoldexVerseChats", m.peer_id)
    if not check_if:
        return await m.reply(
            "Please join @RoldexVerseChats then send me the link again."
        )
    await m.reply(reply_text, link_preview=False, parse_mode="markdown")


@bot.on(
    events.NewMessage(
        pattern="/start (.*)",
        incoming=True,
        outgoing=False,
        func=lambda x: x.is_private,
    )
)
async def start(m: UpdateNewMessage):
    text = m.pattern_match.group(1)
    await handle_start(m, text)


async def handle_start(m: UpdateNewMessage, text: str):
    # Handle start command with arguments
    fileid = None  # This was previously retrieved from the database
    check_if = await is_user_on_chat(bot, "@RoldexVerse", m.peer_id)
    if not check_if:
        return await m.reply("Please join @RoldexVerse then send me the link again.")
    check_if = await is_user_on_chat(bot, "@RoldexVerseChats", m.peer_id)
    if not check_if:
        return await m.reply(
            "Please join @RoldexVerseChats then send me the link again."
        )
    if fileid:
        try:
            await hm.delete()
        except:
            pass

        await bot(
            ForwardMessagesRequest(
                from_peer=PRIVATE_CHAT_ID,
                id=[int(fileid)],
                to_peer=m.chat.id,
                drop_author=True,
                # noforwards=True,  # Uncomment it if you dont want to forward the media.
                background=True,
                drop_media_captions=False,
                with_my_score=True,
            )
        )


@bot.on(
    events.NewMessage(
        pattern="/remove (.*)",
        incoming=True,
        outgoing=False,
        from_users=ADMINS,
    )
)
async def remove(m: UpdateNewMessage):
    # Handle remove command
    pass  # Remove database-related functionality


@bot.on(
    events.NewMessage(
        incoming=True,
        outgoing=False,
        func=lambda message: message.text
        and get_urls_from_string(message.text)
        and message.is_private,
    )
)
async def get_message(m: Message):
    asyncio.create_task(handle_message(m))


async def handle_message(m: Message):

    url = get_urls_from_string(m.text)
    if not url:
        return await m.reply("Please enter a valid url.")
    check_if = await is_user_on_chat(bot, "@RoldexVerse", m.peer_id)
    if not check_if:
        return await m.reply("Please join @RoldexVerse then send me the link again.")
    check_if = await is_user_on_chat(bot, "@RoldexVerseChats", m.peer_id)
    if not check_if:
        return await m.reply(
            "Please join @RoldexVerseChats then send me the link again."
        )
    
    # Rest of the handle_message function remains unchanged

# Start the bot
bot.start(bot_token=BOT_TOKEN)
bot.run_until_disconnected()
