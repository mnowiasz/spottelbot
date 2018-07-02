""" The spotify related functions and constants"""

import functools

import botconfig
import botexceptions
import spotipy.spotipy.client as cl
import spotipy.spotipy.util as util

last_limit = 50

scope = 'user-read-recently-played user-read-currently-playing playlist-read-private'

# Some constants
album_str = "album"
artists_str = "artists"
item_str = "item"
context_str = "context"
name_str = "name"
playlist_str = "playlist"
track_str = "track"
type_str = "type"
uri_str = "uri"


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._token = None
        self._client = None

    def _format_track_object(self, track_object: dict):
        """

        :param track_object: The track object
        :type track_object: dict
        :return: Formatted string
        :rtype: str

        Formats the track object (humand readable)
        """

        fields = ((name_str, ': '), (artists_str, ' ('), (album_str, ') '))

        output = ""
        for field, seperator in fields:
            the_item = track_object[field]
            if isinstance(the_item, list):
                for subitem in the_item:
                    output += subitem[name_str] + seperator
            elif isinstance(the_item, dict):
                output += the_item[name_str] + seperator
            else:
                output += the_item + seperator

        return output

    def _format_context_object(self, context_object: dict):
        """

        :param context_object: The context object
        :type context_object: dict
        :return: Formatted string
        :rtype: str
        """
        output = None

        if context_object[type_str] == playlist_str:
            playlist_uri = context_object[uri_str]
            playlist_dict = self._get_playlist(playlist_uri)
            output = " (Playlist: {}) ".format(playlist_dict[name_str])

        return output

    @functools.lru_cache(maxsize=last_limit)
    def _get_playlist(self, uri: str):
        """

        :param uri: The URI of the playlist ("spotfiy:...")
        :type uri: str
        :return: The dictonary of fields
        :rtype: dict

        Gets the playlist details (formatting it)
        """
        playlist_object = self._client.user_playlist(self._config._spotify_username, uri, fields=name_str)
        return playlist_object

    def get_playlist(self, uri: str) -> str:
        """

        :param uri: The URI of the playlist
        :type uri: str
        :return: name of the playlist
        :rtype: str

        Returns the name of the playlist (formatted string)
        """

        playlist_name = "<unknown>"

        playlist_object = self._get_playlist(uri)

        if playlist_object:
            playlist_name = playlist_object[name_str]

        return playlist_name

    @functools.lru_cache(maxsize=last_limit)
    def get_track(self, uri: str) -> str:
        """

        :param uri: The spotify URI for the track
        :type uri: str
        :return: formatted string
        :rtype: str

        Returns the track in humand readable form
        """
        output = "<unknown>"
        track_object = self._client.track(uri)

        if track_object:
            output = self._format_track_object(track_object)

        return output

    def connect(self):
        config = self._config
        self._token = util.prompt_for_user_token(config._spotify_username, scope, config._spotify_client_id,
                                                 config._spotify_client_secret, config._spotify_redirect_uri)
        if not self._token:
            raise botexceptions.SpotifyAuth

        self._client = cl.Spotify(auth=self._token)

    def get_current(self, formatted=True):
        """
        :param formatted: If true, returns a string. If false,returns a tuple of spotify ids
        :return: tuple of track_id and playlist_id (formatted = false) or string (formatted=true)
        :rtype: tuple

        Returns the currently playing song (if any).
        """

        currently_playing_object = self._client.current_user_playing_track()

        if formatted:
            ret_object = None
        else:
            ret_object = (None, None)

        if currently_playing_object:
            the_item = currently_playing_object.get(item_str)
            the_context = currently_playing_object.get(context_str)
            if the_item:
                if formatted:
                    output = self._format_track_object(the_item)
                    if the_context:
                        output += self._format_context_object(the_context)
                    ret_object = output
                else:
                    context_id = None
                    if the_context:
                        if the_context[type_str] == playlist_str:
                            context_id = the_context[uri_str]
                    track_id = the_item[uri_str]
                    ret_object = (track_id, context_id)

        return ret_object

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
            output_list.append(self._format_track_object(play_history_object[track_str]) + self._format_context_object(
                play_history_object[context_str]))

        return output_list

    def get_last_index(self, index: int):
        """

        :param index: Recently played titles's index (< last_limit)
        :type index: int
        :return: track_id, playlist_id
        :rtype: tuple

        return the recently played track (1 == the last played track before current, up to last_limit). Raises an
        IndexError if index > last_limit

        """

        if index < 1 or index > last_limit:
            raise botexceptions.InvalidRange(index)

        play_history = self._get_last_play_history_objects(index - 1, index - 1)

        track_id = None
        playlist_id = None

        if play_history:
            item = play_history[0]
            track_id = item[track_str][uri_str]
            context = item[context_str]
            if context[type_str] == playlist_str:
                playlist_id = context[uri_str]

        return track_id, playlist_id
