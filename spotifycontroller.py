""" The spotify related functions and constants"""

import functools

import botconfig
import botexceptions
import spotipy.spotipy.client as cl
import spotipy.spotipy.util as util

last_limit = 50

scope = 'user-read-recently-played user-read-currently-playing playlist-read-private'


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._token = None
        self._client = None

    def _format_play_history_object(self, play_history_object: dict):
        """

        :param play_history_object: The PHO in question
        :type play_history_object: dict
        :return: Formatted string
        :rtype: str

        Formats the PHO so it's human readable
        """

        fields = (('name', ': '), ('artists', ' ('), ('album', ') '))

        output = ""
        for field, seperator in fields:
            the_item = play_history_object['track'][field]
            if isinstance(the_item, list):
                for subitem in the_item:
                    output += subitem['name'] + seperator
            elif isinstance(the_item, dict):
                output += the_item['name'] + seperator
            else:
                output += the_item + seperator

        # If it's part of a playlist, display the playlist. If not, display the album
        context = play_history_object['context']
        if context['type'] == 'playlist':
            playlist_uri = context['uri']
            playlist_dict = self._get_playlist(playlist_uri)
            output += "Playlist " + playlist_dict['name']
        elif context['type'] == 'album':
            output += "Album " + play_history_object['track']['album']['name']

        return output

    @functools.lru_cache(maxsize=128)
    def _get_playlist(self, uri: str):
        """
        :param uri: The URI of the playlist ("spotfiy:...")
        :type uri: str
        :return: The dictonary of fields
        :rtype: dict

        Gets the playlist details (formatting it)
        """

        playlist_object = self._client.user_playlist(self._config._spotify_username, uri, fields="name")
        return playlist_object

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

    def _get_last_play_history_objects(self, lower: int, upper: int):
        """

        :param lower: the lower index (range 0..last_limit-1
        :type lower: int
        :param upper: the upper index (range 0..last-limit-1), >=lower
        :type upper: int
        :return: list of PHOs
        :rtype: list

        Returns the list of tracks defined by lower and upper index
        """

        return self._client.current_user_recently_played(upper + 1)["items"][lower:upper + 1]

    def get_last_tracks(self, lower: int, upper: int):
        """

        :param lower: The lower index (range 1..last_limit)
        :type lower:  int
        :param upper: the upper index (range 1..last_limit), >= upper
        :type upper: int
        :return: A list of formatted strings
        :rtype: list

        Returns a list of formatted strings containing the recently played tracks
        """

        output_list = []
        pho_list = self._get_last_play_history_objects(lower - 1, upper - 1)

        for play_history_object in pho_list:
            output_list.append(self._format_play_history_object(play_history_object))

        return output_list

    def get_last_index(self, index: int):
        """

        :param index: Recently played titles's index (< last_limit)
        :type index: int
        :return: track_id, playlist_id
        :rtype: tuple

        return the recently played track (0 == the last played track before current, up to last_limit). Raises an
        IndexError if index > last_limit

        """

        play_history = self._get_last_play_history_objects(index, index)

        print(self._format_play_history_object(play_history[0]))

        # TODO: Functionality
        return (None, None)
