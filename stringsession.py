
import sys
import asyncio
from pyrogram import Client

from config import API_ID, API_HASH
from spotify_tg.logging import LOGGER

async def create_session():
    async with Client(
        "user_client",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    ) as app:
        stringsession = await app.export_session_string()
        await app.send_message(
            "me",
            f"""
**STRING_SESSION:**
```
{stringsession}
```

⚠️ **Do not share with anyone**
            """
        )

if __name__ == "__main__":
    try:
        asyncio.run(create_session())
    except Exception as e:
        LOGGER(__name__).error(e)
        sys.exit()
