
import os

from pyrogram import Client, enums
from pyrogram.errors import MessageNotModified, MessageIdInvalid
from pyrogram.types import (
    Message,
    CallbackQuery,
    InputMediaPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from .database import Database
from .utils import SpotifyNow, SpotifyDown
from config import CHAT_ID


db = Database()
now = SpotifyNow()
down = SpotifyDown()

last_song = None
message_id = None


def r_markup(result):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🎧 Open Spotify",
                    url=result["song_url"]
                ),
                InlineKeyboardButton(
                    text="🎧 Other",
                    url=f"https://song.link/s/{result['song_id']}"
                )
            ]
        ]
    )


async def handle_callback_query(c: Client, q: CallbackQuery):
    if q.data.startswith("delete_"):
        message_id = q.data.split("_")[1]
        await c.delete_messages(CHAT_ID, int(message_id))
        await q.answer("The song has been deleted successfully.")
        await q.message.delete()
    elif q.data == "ignore":
        await q.message.delete()


async def check_and_add_song(c: Client, m: Message):
    audio = m.audio
    full_track = f"{audio.performer} - {audio.title}"

    if not db.is_downloaded(full_track):
        db.downloaded(full_track)
    else:
        await m.reply_text(
            "This song already exists.\nDo you want to delete it?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Delete", callback_data=f"delete_{m.id}"
                        ),
                        InlineKeyboardButton(
                            "Ignore", callback_data="ignore"
                        )
                    ]
                ]
            )
        )


async def process_audio_messages(c):
    async for m in c.search_messages(
        CHAT_ID,
        filter=enums.MessagesFilter.AUDIO
    ):
        audio = m.audio
        full_track = f"{audio.performer} - {audio.title}"

        db.downloaded(full_track)


async def send_song(c):
    result = now.current_song()
    if result != "paused":
        if not db.is_downloaded(result["full_track"]):
            db.downloaded(result["full_track"])
            link = result["song_url"]
        else:
            link = False

        if link:
            track = await down.download_song(link)
            await c.send_audio(
                chat_id=CHAT_ID,
                audio=track,
                caption=f"[Spotify]({link}) | [Other](https://song.link/s/{result['song_id']})"
            )
            os.remove(track)


async def edit_message(c):
    global last_song
    global message_id

    result = now.current_song()

    if result != "paused":
        if message_id is None:
            message_id = await send_post(c, result)

        if result["full_track"] != last_song:
            try:
                await c.edit_message_media(
                    chat_id=CHAT_ID,
                    message_id=message_id,
                    media=InputMediaPhoto(
                        result["cover_art"]
                    )
                )
        
                await c.edit_message_caption(
                    chat_id=CHAT_ID,
                    message_id=message_id,
                    caption=f"🎧 **{result['full_track']}**",
                    reply_markup=r_markup(result)
                )
        
                last_song = result["full_track"]
            except (MessageNotModified, MessageIdInvalid):
                message_id = await send_post(c, result)


async def send_post(c, result):
    m = await c.send_photo(
        chat_id=CHAT_ID,
        photo=result["cover_art"],
        caption=f"🎧 **{result['full_track']}**",
        reply_markup=r_markup(result)
    )
    await m.pin()

    return m.id
