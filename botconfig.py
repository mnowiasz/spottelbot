""" Bot's config """

import configparser

import botexceptions

"""Both a bookmark name and a value (Currently playing)"""
bookmark_current = "current"

""" /delete all, /clear all"""
bookmark_all = "all"


# Make sure that "current" is first in list. After that, the list can be sorted
def _bookmark_compare(key):
    if key == bookmark_current:
        return " "
    else:
        return key


def _check_telegram_id(telegram_id: str):
    """

    :param telegram_id: The telegram ID
    :type telegram_id: str
    :return:
    :rtype:

    Checks if the telegram id is valid. Will raise and InvalidUser exception if not
    """
    illegal = False

    if not telegram_id.isdigit():
        if not telegram_id.startswith("@"):
            illegal = True
        elif len(telegram_id) == 1:  # Only one @
            illegal = True

    if illegal:
        raise botexceptions.InvalidUser(telegram_id)


class BotConfig(object):
    _telegram_section = "telegram"
    _telegram_entry_token = "token"
    _telegram_entry_users = "users"
    _spotify_section = "spotify"
    _spotify_entry_username = "username"
    _spotify_entry_client_id = "client_id"
    _spotify_entry_client_secret = "client_secret"
    _spotify_entry_redirect_uri = "redirect_uri"
    _bookmark_section = "bookmarks"
    _config_file = None

    def __init__(self):
        self._config = None
        self.access = set()
        self.bookmarks = {}
        self._translation_table = dict.fromkeys(map(ord, " \t"), "_")

    def _load_telegram_config(self):
        """
        Loads telegram's config items
        """

        self.telegram_token = self._config[self._telegram_section][self._telegram_entry_token.strip()]
        if self.telegram_token == "":
            raise botexceptions.MissingTelegramToken()
        self.clear_access()
        users = self._config[self._telegram_section][self._telegram_entry_users]
        if users == "":
            raise botexceptions.MissingUsers

        for telegram_id in users.split(","):
            stripped = telegram_id.strip()
            try:
                self.add_access(stripped)
            # A KeyError in add_access() can only mean that a user ID already exist
            except KeyError as k:
                raise botexceptions.DuplicateUsers(stripped) from k

    def _load_spotify_config(self):
        """

        Loads spotify's config items
        """

        self._spotify_username = self._config[self._spotify_section][self._spotify_entry_username]
        if self._spotify_username == "":
            raise botexceptions.MissingSpotifyUsername()
        self._spotify_client_id = self._config[self._spotify_section].get(self._spotify_entry_client_id)
        self._spotify_client_secret = self._config[self._spotify_section].get(self._spotify_entry_client_secret)
        self._spotify_redirect_uri = self._config[self._spotify_section].get(self._spotify_entry_redirect_uri)

    def _load_bookmarks(self):
        """

        Loads the bookmarks
        """

        self.clear_bookmarks()
        for bookmark_name, entry in self._config[self._bookmark_section].items():
            splitted = entry.split(",")
            track_id = splitted[0].strip()

            if track_id == "" or len(splitted) > 2:
                raise botexceptions.InvalidBookmark(bookmark_name)
            elif len(splitted) == 1:
                playlist_id = None
            else:
                playlist_id = splitted[1].strip()
            self.set_bookmark(bookmark_name, track_id, playlist_id)

    def load_config(self, configfile):
        """

        :param configfile: The file to parse
        :type configfile: filelike object
        :return:
        :rtype:

        Loads/reload the config stored in the file. Throws the usual exceptions
        """

        self._config = configparser.ConfigParser()
        self._config.read_file(configfile)

        # Reset fd so a reload won't do harm. On the other hand, the file in question could be changed so the
        # filehandle would be invalid. But can't harm

        configfile.seek(0)
        try:
            self._load_telegram_config()
            self._load_spotify_config()
            if self._bookmark_section in self._config:
                self._load_bookmarks()

        # Transform generic exceptions into more specific ones which are more easily processed, resulting in more
        # readable code
        except KeyError as key_error:
            missing_key = key_error.args[0]
            if missing_key == self._telegram_section or missing_key == self._spotify_section:
                raise botexceptions.MissingSection(missing_key) from key_error
            elif missing_key == self._telegram_entry_token:
                raise botexceptions.MissingTelegramToken from key_error
            elif missing_key == self._telegram_entry_users:
                raise botexceptions.MissingUsers from key_error
            elif missing_key == self._spotify_entry_username:
                raise botexceptions.MissingSpotifyUsername from key_error
            else:
                # DuplicateSectionError, DuplicateOption...
                raise
        self._config_file = configfile

    def _save_telegram(self):
        """
        Saves the telegram section
        """

        self._config.remove_section(self._telegram_section)
        self._config.add_section(self._telegram_section)
        self._config[self._telegram_section][self._telegram_entry_token] = self.telegram_token
        if self.access:
            self._config[self._telegram_section][self._telegram_entry_users] = \
                ",".join(str(telegram_id) for telegram_id in self.access)

    def _save_spotify(self):
        """

        Saves the spotify section
        """

        self._config.remove_section(self._spotify_section)
        self._config.add_section(self._spotify_section)
        self._config[self._spotify_section][self._spotify_entry_username] = self._spotify_username

        if self._spotify_client_id:
            self._config[self._spotify_section][self._spotify_entry_client_id] = self._spotify_client_id

        if self._spotify_client_secret:
            self._config[self._spotify_section][self._spotify_entry_client_secret] = self._spotify_client_secret

        if self._spotify_redirect_uri:
            self._config[self._spotify_section][self._spotify_entry_redirect_uri] = self._spotify_redirect_uri

    def _save_bookmarks(self):
        """

        Saves the bookmark section
        """

        if self._config.has_section(self._bookmark_section):
            self._config.remove_section(self._bookmark_section)
        self._config.add_section(self._bookmark_section)
        for bookmark in self.get_bookmarks():
            track_id, playlist_id = self.get_bookmark(bookmark)
            if playlist_id is None:
                self._config[self._bookmark_section][bookmark] = track_id
            else:
                self._config[self._bookmark_section][bookmark] = track_id + "," + playlist_id

    def save_config(self, configfile):
        """

        :param configfile: The file like object to write the config into. If None, the last file (loaded/saved) will be used
        :type configfile: File
        :return:
        :rtype:

        Write the config into the specified configfile
        """

        the_file = configfile

        if not configfile:
            the_file = self._config_file

        the_file.seek(0)
        self._save_telegram()
        self._save_spotify()
        self._save_bookmarks()
        self._config.write(the_file)
        the_file.truncate()
        the_file.seek(0)


    def has_access(self, telegram_id: str) -> bool:
        """
        :param telegram_id: The telegram ID (either numeric or "@..")
        :type telegram_id: str
        :return: if the telegram ID is allowed to query the bot
        :rtype: bool
        Checks if the telegram ID is allowed to talk to the bot
        """
        return telegram_id in self.access

    def add_access(self, telegram_id: str):
        """
        :param telegram_id: the telegram ID (either numeric or "@..")
        :type telegram_id: str
        Adds an entry to the list of allowed user ids. Raises a KeyError if the ID is already present.
        Raises an IllegalUsername when the telegram_id is not numeric and doesn't start with an @
        """
        _check_telegram_id(telegram_id)
        if self.has_access(telegram_id):
            raise KeyError(telegram_id)

        self.access.add(telegram_id)

    def remove_access(self, telegram_id: str):
        """
        :param telegram_id: the telegram ID
        :type telegram_id: str
        Removes the entry from the list of allowed user ids. Raises a KeyError if the ID is not present
        Raises an IllegalUsername when the telegram_id is not numeric and doesn't start with an @
        """

        # No need to check the ID. Since add_access checks, the (illegal) ID can't be here.
        self.access.remove(telegram_id)

    def clear_access(self):
        """
        Empties the access list/dictionary. Used in (re)loading the config
        """
        self.access = set()

    def _sanitize_bookmark(self, bookmark_string: str) -> str:
        """
        :param bookmark_string: The string to sanitize
        :type bookmark_string: str
        :return: The sanitized string
        :rtype: str
        Removes trailing/leading spaces, and replaces certain characters (like spaces to underscores). Also transforms
        to lower
        """

        return bookmark_string.strip().translate(self._translation_table).lower()

    def set_bookmark(self, bookmark_name: str, track_id: str, playlist_id: str = None):
        """
        :param bookmark_name: The name of the bookmark ("current", "foo", "bar"..).
        :type bookmark_name: str
        :param track_id: Spotify's track ID - base62 coded
        :type track_id: str
        :param playlist_id: The (optional) playlist ID - base62 coded
        :type playlist_id: str
        Sets a bookmark. If already present, the bookmark will be overwritten. If the name is a numeric value, an
        InvalidBookmark will be raised, because otherwise it would be very confusing setting a numeric bookmark to
        a numeric value (last tracks's list). "all" is also an invalid bookmark name, as in /delete all
        """

        sanitzed = self._sanitize_bookmark(bookmark_name)

        # "5" or "all"
        if sanitzed.isdigit() or sanitzed == bookmark_all:
            raise botexceptions.InvalidBookmark(sanitzed)

        self.bookmarks[self._sanitize_bookmark(bookmark_name)] = (track_id, playlist_id)

    def get_bookmark(self, bookmark_name: str) -> (str, str):
        """
        :param bookmark_name: The name of the bookmark ("current", "a")
        :type bookmark_name: str
        :return: The ID of the track and (optionally) playlist
        :rtype: (str, str)
        Gets a bookmark. If the name of the bookmark doesn't exist a KeyError will be raised
        """
        return self.bookmarks[self._sanitize_bookmark(bookmark_name)]

    def clear_bookmark(self, bookmark_name: str):
        """
        :param bookmark_name: The name of the bookmark ("current", "a")
        :type bookmark_name: str
        Clears the bookmark. If the bookmark doesn't exist a KeyError will be raised
        """

        del self.bookmarks[self._sanitize_bookmark(bookmark_name)]

    def get_bookmarks(self) -> list:
        """
        :return The sorted list of bookmarks
        :rtype list
        Returns the name of the bookmarks in a sorteds list, with "current" as the first entry
        """
        return sorted(self.bookmarks.keys(), key=_bookmark_compare)

    def clear_bookmarks(self):
        """
        :return:
        :rtype:
        Empties the bookmark list, either by command or by reloading the config
        """

        self.bookmarks = {}
