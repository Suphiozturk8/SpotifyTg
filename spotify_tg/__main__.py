
import os
import asyncio
import logging

from pyrogram import filters, idle
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import CHAT_ID, USER_BOT
from .clients import BotClient, UserClient
from .database import Database
from .handlers import (
    check_and_add_song,
    spotify_to_telegram,
    handle_callback_query,
    process_audio_messages
)


async def run_audio_processing():
    user_client = UserClient()
    await user_client.start()
    await process_audio_messages(user_client)
    await user_client.stop()


async def main():
    bot_client = BotClient()

    if not os.path.exists("songs.db"):
        db = Database()
        db.initialize()

        if USER_BOT:
            await run_audio_processing()

    await bot_client.start()

    bot_client.add_handler(
        handler=MessageHandler(
            check_and_add_song,
            filters=filters.incoming
            & filters.audio
            & filters.chat(CHAT_ID)
        )
    )

    bot_client.add_handler(
        handler=CallbackQueryHandler(
            handle_callback_query
        )
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        spotify_to_telegram,
        "interval",
        seconds=40,
        args=[bot_client],
        max_instances=2
    )
    scheduler.start()

    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
