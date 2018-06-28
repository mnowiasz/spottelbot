""" The spotify related functions and constants"""

import botconfig
import botexceptions
import spotipy.spotipy.client as cl
import spotipy.spotipy.util as util

last_limit = 50
scope = 'user-read-recently-played user-read-currently-playing'


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._token = None
        self._client = None

    def _format_track(self, track: dict):
        """

        :param track: The track in question
        :type track: dict
        :return: Formatted string
        :rtype: str

        Formats the track so it's human readable
        """

        fields = (('name', ': '), ('artists', ' ('), ('album', ') '))
        output = ""

        for field, seperator in fields:
            the_item = track[field]
            if isinstance(the_item, list):
                for subitem in the_item:
                    output += subitem['name'] + seperator
            elif isinstance(the_item, dict):
                output += the_item['name'] + seperator
            else:
                output += the_item + seperator
        return output

    def connect(self):
        config = self._config
        self._token = util.prompt_for_user_token(config._spotify_username, scope, config._spotify_client_id,
                                                 config._spotify_client_secret, config._spotify_redirect_uri)
        if not self._token:
            raise botexceptions.SpotifyAuth

        self._client = cl.Spotify(auth=self._token)

    def get_current(self):
        """

        :return: tuple of track_id and playlist_id
        :rtype: tuple

        Returns the currently playing song (if any).
        """

        track = self._client.current_user_playing_track()


        return (None, None)
        # TODO: Functionality

    def _get_last_tracks(self, lower: int, upper: int):
        """

        :param lower: the lower index (range 0..last_limit-1
        :type lower: int
        :param upper: the upper index (range 0..last-limit-1), >=lower
        :type upper: int
        :return: list of tracks
        :rtype: list

        Returns the list of tracks defined by lower and upper index
        """

        return self._client.current_user_recently_played(upper + 1)["items"][lower:upper + 1]


    def get_last_index(self, index: int):
        """

        :param index: Recently played titles's index (< last_limit)
        :type index: int
        :return: track_id, playlist_id
        :rtype: tuple

        return the recently played track (0 == the last played track before current, up to last_limit). Raises an
        IndexError if index > last_limit

        """

        tracks = self._get_last_tracks(index, index)

        print(self._format_track(tracks[0]['track']))

        return (None, None)
