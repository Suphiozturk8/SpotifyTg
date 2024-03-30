
# My Spotify Music Bot

## Overview
This Telegram bot allows users to download songs from Spotify and share currently playing songs in a Telegram chat. It utilizes the Pyrogram library for interacting with the Telegram API and SQLite database for managing downloaded songs.

## Features
- Download songs from Spotify.
- Share currently playing songs in a Telegram chat.
- Automatically delete duplicate songs.

## Screenshots
1. Song Playing on Spotify:
   ![Song Playing on Spotify](https://telegra.ph/file/06296158a21302616ac81.jpg)
   In this screenshot, you can see the song currently playing on Spotify.
2. Currently Playing and Downloaded Song:
   ![Downloaded Song](https://telegra.ph/file/5150ef5183d7875716d07.jpg)
   In this screenshot, you can see that the song currently playing on Spotify is shared and downloaded on the Telegram channel.

## Configuration
Before running the bot, configure the following settings in the `config.py` file:
- [Spotify API](https://developer.spotify.com/dashboard/applications) credentials
- [Telegram API](https://my.telegram.org/) credentials
- Bot settings (e.g., `USER_BOT`, `STRING_SESSION`, `CHAT_ID`, `WORKERS`)

## UserBot Configuration
In the `config.py` file, there is a parameter named `USER_BOT` which determines whether the userbot mode should be activated in addition to the bot mode.

- When `USER_BOT` is set to `True`:
  - Both the bot and the userbot modes will be active.
  - The userbot mode will be activated and songs previously sent in the channel specified by `CHAT_ID` will be prevented from being resent by saving them to the database.
  - It will require providing the session string (`STRING_SESSION`) specified in the `config.py` file. To get it, run this command:
    ```bash
    python stringsession.py
    ```

- When `USER_BOT` is set to `False`:
  - Only the bot mode will be active.
  - The bot will run without activating the userbot mode.
  - If there are songs previously sent in the channel specified by `CHAT_ID`, the bot may resend them.

## Logging
Log messages are formatted with colors indicating the log level.
By default, log messages are printed to the console.
You can enable file logging by setting the `LOG_TO_FILE` parameter to `True` in the `config.py` file and specifying the log file path using the `LOG_FILE_PATH` parameter.

Make sure to configure the `config.py` file according to your preference before running the bot.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/suphiozturk8/SpotifyTg.git && cd SpotifyTg
   ```
2. Create a virtual environment and activate it:
   - Windows:
     ```bash
     python -m venv myenv
     myenv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     python -m venv myenv
     source myenv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your configurations in the `config.py` file.
5. Run the bot:
   ```bash
   python -m spotify_tg
   ```

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes and commit: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
