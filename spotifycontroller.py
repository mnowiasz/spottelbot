""" The spotify related functions and constants"""

import botconfig

last_limit = 50


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._token = None

    def connect(self):
        pass


    def get_current(self):
        """

        :return: tuple of track_id and playlist_id
        :rtype: tuple

        Returns the currently playing song (if any).
        """
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
