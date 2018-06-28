""" The spotify related functions and constants"""

import botconfig
import botexceptions
import spotipy.spotipy as spotipy
import spotipy.spotipy.util as util

last_limit = 50
scope = 'user-read-recently-played user-read-currently-playing'


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._token = None
        self._client = None

    def connect(self):
        config = self._config
        self._token = util.prompt_for_user_token(config._spotify_username, spotipy, config._spotify_client_id,
                                                 config._spotify_client_secret, config._spotify_redirect_uri)
        if not self._token:
            raise botexceptions.SpotifyAuth

        self._client = spotipy.Spotipy(auth=self._token)

    def get_current(self):
        """

        :return: tuple of track_id and playlist_id
        :rtype: tuple

        Returns the currently playing song (if any).
        """

        track = self._client.current_user_playing_track()

        print(track)

        return (None, None)

    def get_last_index(self, index: int):
        """

        :param index: Recently played titles's index (< last_limit)
        :type index: int
        :return: track_id, playlist_id
        :rtype: tuple

        return the recently played track (0 == the last played track before current, up to last_limit). Raises an
        IndexError if index > last_limit

        """

        return (None, None)
