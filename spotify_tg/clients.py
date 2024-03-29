
import sys

from pyrogram import Client

from .logging import LOGGER
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, CHAT_ID

class BotClient(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting BotClient...")
        super().__init__(
            "bot_client",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            msg = await self.send_message(
                CHAT_ID, "BotClient Started"
            )
            await self.delete_messages(CHAT_ID, msg.id)
        except:
            LOGGER(__name__).error(
                f"Bot has failed to access the channel ({CHAT_ID}). Make sure that you have added your bot to your channel and promoted as admin!"
            )
            sys.exit()

        a = await self.get_chat_member(CHAT_ID, self.id)
        if a.status == "ChatMemberStatus.ADMINISTRATOR":
            LOGGER(__name__).warning(
                "Please promote Bot as Admin in Channel"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(
            f"BotClient Started as {self.name}"
        )


class UserClient(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting UserClient...")
        super().__init__(
            "user_client",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=STRING_SESSION,
            no_updates=True
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            msg = await self.send_message(
                CHAT_ID, "UserClient Started"
            )
            await self.delete_messages(CHAT_ID, msg.id)
        except:
            LOGGER(__name__).error(
                f"UserBot has failed to access the channel ({CHAT_ID}). Make sure that you have added your UserBot to your channel and promoted as admin!"
            )
            sys.exit()

        a = await self.get_chat_member(CHAT_ID, self.id)
        if a.status == ("ChatMemberStatus.OWNER" or "ChatMemberStatus.ADMINISTRATOR"):
            LOGGER(__name__).warning(
                "Please promote UserBot as Admin in Channel"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(
            f"UserClient Started as {self.name}"
        )
