""" The spotify related functions and constants"""

import datetime
import functools

import dateutil.parser
import dateutil.tz

import spotipy.spotipy.client as cl
import spotipy.spotipy.util as util
from spottelbot import botconfig
from spottelbot import botexceptions

# Theoretically it's possible to have mor than 50 last items by using the "next" feature. But since 50 entries
# makes quite a list (especially when using the mobile telegram client), this limit shouldn't bother anyone - it's
# a matter of convenience

last_limit = 50

scope = 'user-read-recently-played user-read-currently-playing playlist-read-private'

# Some constants
album_str = "album"
artists_str = "artists"
item_str = "item"
items_str = "items"
context_str = "context"
name_str = "name"
playlist_str = "playlist"
track_str = "track"
type_str = "type"
uri_str = "uri"
played_at_str = "played_at"


class SpotifyController(object):

    def __init__(self, config: botconfig.BotConfig):
        self._config = config
        self._oath = None
        self._client = None

    def __format_context_object(self, context_object: dict):
        """

        :param context_object: The context object
        :type context_object: dict
        :return: Formatted string
        :rtype: str

        Formats the context object. A context object describes the context the track was played from (playlist, album..)
        Currently only the playlist is supported, the album is usually already part of the track object
        """
        formatted_context = ""

        if context_object:
            if context_object[type_str] == playlist_str:
                playlist_uri = context_object[uri_str]
                playlist_dict = self.__get_playlist(playlist_uri)
                formatted_context = " (Playlist: {}) ".format(playlist_dict[name_str])

        return formatted_context

    def _format_played_at(self, played_at_object: str) -> str:
        """

        :param played_at_object: The content of 'played_at'
        :return: Formatted string

        Formats the play_at_object ("2018-07-06T..."), returns the formatted string
        """

        local_tz = dateutil.tz.tzlocal()
        date_time = dateutil.parser.parse(played_at_object).astimezone(local_tz)

        date_string = ""

        today = datetime.date.today()
        date_played_at = date_time.date()

        delta = today - date_played_at

        if delta.days == 0:
            date_string = "Today"
        else:
            if delta.days == 1:
                date_string = "Yesterday"
            else:
                format_string = ""
                if delta.days <= 6:
                    format_string = "%a"
                else:
                    format_string = "%x"
                date_string = datetime.datetime.strftime(date_time, format_string)
            
        return date_string + " " + datetime.datetime.strftime(date_time, "%X")

    def __format_track_object(self, track_object: dict):
        """

        :param track_object: The track object
        :type track_object: dict
        :return: Formatted string
        :rtype: str

        Formats the track object (human readable)
        """

        fields = ((name_str, ': '), (artists_str, ' ('), (album_str, ') '))

        formatted_track = ""
        for field, seperator in fields:
            the_item = track_object[field]
            if isinstance(the_item, list):
                for subitem in the_item:
                    formatted_track += subitem[name_str] + seperator
            elif isinstance(the_item, dict):
                formatted_track += the_item[name_str] + seperator
            else:
                formatted_track += the_item + seperator

        return formatted_track

    # Since a playlist (at least the name) usually doesn't change that often and this method is being called
    # by the bookmark functions (usually more than once), it can be cached so we don't get any spotify rate limit.
    # The drawback: If the user changes the playlist's name, the old name would be displayed. So it's a trade off
    @functools.lru_cache(maxsize=last_limit)
    def __get_playlist(self, uri: str):
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

        playlist_object = self.__get_playlist(uri)

        if playlist_object:
            playlist_name = playlist_object[name_str]

        return playlist_name

    # A track name shouldn't change at all - so it's safe to use a cache therefore reducing the requests to spotify
    @functools.lru_cache(maxsize=last_limit)
    def get_track(self, uri: str) -> str:
        """

        :param uri: The spotify URI for the track
        :type uri: str
        :return: formatted string
        :rtype: str

        Returns the track in humand readable form
        """
        formatted_track = "<unknown>"
        track_object = self._client.track(uri)

        if track_object:
            formatted_track = self.__format_track_object(track_object)

        return formatted_track

    def connect(self):
        """
        Connect to spotify - the user will be asked to enter the URL send by spotify after authorizing the client
        :return:
        :rtype:
        """

        config = self._config
        self._oath = util.prompt_for_oauth_object(config._spotify_username, scope, config._spotify_client_id,
                                                  config._spotify_client_secret, config._spotify_redirect_uri)

        if not self._oath:
            raise botexceptions.SpotifyAuth

        self._client = cl.Spotify(client_credentials_manager=self._oath)

    def get_current(self, formatted=True):
        """
        :param formatted: If true, returns a string. If false,returns a tuple of spotify ids
        :return: tuple of track_id and playlist_id (formatted = false) or string (formatted=true)
        :rtype: tuple or string

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
                    formatted_output = self.__format_track_object(the_item)
                    if the_context:
                        formatted_output += self.__format_context_object(the_context)
                    ret_object = formatted_output
                else:
                    context_id = None
                    if the_context:
                        if the_context[type_str] == playlist_str:
                            context_id = the_context[uri_str]
                    track_id = the_item[uri_str]
                    ret_object = (track_id, context_id)

        return ret_object

    def __get_last_play_history_objects(self, lower: int, upper: int):
        """

        :param lower: the lower index (range 0..last_limit-1
        :type lower: int
        :param upper: the upper index (range 0..last-limit-1), >=lower
        :type upper: int
        :return: list of PHOs
        :rtype: list

        Returns the list of tracks defined by lower and upper index
        """
        return self._client.current_user_recently_played(upper + 1)[items_str][lower:upper + 1]

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

        formatted_tracks_list = []
        pho_list = self.__get_last_play_history_objects(lower - 1, upper - 1)

        for play_history_object in pho_list:
            played_at_string = self._format_played_at(play_history_object[played_at_str])
            formatted_tracks_list.append(
                self.__format_track_object(play_history_object[track_str]) + self.__format_context_object(
                    play_history_object[context_str]) + " - " + played_at_string)

        return formatted_tracks_list

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

        play_history = self.__get_last_play_history_objects(index - 1, index - 1)

        track_id = None
        playlist_id = None

        if play_history:
            item = play_history[0]
            track_id = item[track_str][uri_str]
            context = item[context_str]
            if context[type_str] == playlist_str:
                playlist_id = context[uri_str]

        return track_id, playlist_id
