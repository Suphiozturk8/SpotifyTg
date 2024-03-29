
import os
import sys

from typing import Union
from pathlib import Path

from spotdl.search import spotifyClient
from spotdl.search.songObj import SongObj
from spotdl.download.downloader import DownloadManager

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from .logging import LOGGER
from .executor import run_in_thread
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USER_NAME


class SpotifyDown:
    def __init__(self):
        self.clientId = CLIENT_ID
        self.clientSecret = CLIENT_SECRET

    def init_client(self) -> None:
        try:
            spotifyClient.initialize(
                clientId=self.clientId,
                clientSecret=self.clientSecret
            )
        except Exception as e:
            LOGGER(__name__).error(e)
            pass

    async def download_song(
        self, url: Union[str, SongObj]
    ) -> Path:
        if not os.path.exists(".cache"):
            self.init_client()

        song = url
        if not isinstance(url, SongObj):
            song = await run_in_thread(
                SongObj.from_url
            )(song)

        return await DownloadManager().download_song(song)

class SpotifyNow:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI
        self.username = USER_NAME

    def auth_enticate(self):
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            username=self.username,
            scope="user-read-currently-playing",
            open_browser=False,
            show_dialog=True
        )

        if not os.path.exists(f".cache-{self.username}"):
            auth_url = auth_manager.get_authorize_url()

            LOGGER(__name__).warning(
                f"\nSpotify authorization not done!\nPlease go to the link and complete the authorization:\n{auth_url}"
            )

            auth_input = input(
                "\nPlease enter the authorization code you received after completing the authorization process: "
                f"\n(You should have been redirected to a URL starting with '{self.redirect_uri}?code=' followed by some characters)\n>> "
            )

            try:
                token = auth_manager.parse_auth_response_url(
                    url=auth_input
                )
                auth_manager.get_access_token(
                    token,
                    as_dict=False,
                    check_cache=False
                )
            except Exception as e:
                LOGGER(__name__).error(e)
                sys.exit()

            LOGGER(__name__).info(
                "\nSpotify authorization successful."
            )

        return auth_manager

    def current_song(self):
        auth_manager = self.auth_enticate()

        spotify_instance = Spotify(
            auth_manager=auth_manager
        )
        result = spotify_instance.current_user_playing_track()
        if result:
            song_url = result["item"]["external_urls"]["spotify"]
            song_id = result["item"]["id"]
            cover_art = result["item"]["album"]["images"][1]["url"]
            artist = result["item"]["artists"][0]["name"]
            track_name = result["item"]["name"]
            full_track = f"{artist} - {track_name}"

            data = {
                "song_url": song_url,
                "song_id": song_id,
                "full_track": full_track,
                "cover_art": cover_art
            }
            return data
        else:
            return "paused"

