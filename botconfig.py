""" Bot's config """

import configparser

import botcontroller
import botexceptions


class BotConfig(object):
    _telegram_section = "telegram"
    _telegram_entry_token = "token"
    _telegram_entry_users = "users"
    _spotify_section = "spotify"
    _spotify_entry_username = "username"
    _bookmark_section = "bookmarks"

    def __init__(self, controller: botcontroller):
        self._controller = controller
        self._config = None

    def _load_telegram_config(self):
        """
        Loads telegram's config items
        """

        self._telegram_token = self._config[self._telegram_section][self._telegram_entry_token.strip()]
        if self._telegram_token == "":
            raise botexceptions.MissingTelegramToken()
        self._controller.clear_access()
        users = self._config[self._telegram_section][self._telegram_entry_users]
        if users == "":
            raise botexceptions.MissingUsers

        for telegram_id in users.split(","):
            stripped = telegram_id.strip()
            try:
                self._controller.add_access(stripped)
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

    def _load_bookmarks(self):
        """

        Loads the bookmarks
        """

        self._controller.clear_bookmarks()
        for bookmark_name, entry in self._config[self._bookmark_section].items():
            splitted = entry.split(",")
            track_id = splitted[0].strip()

            if track_id == "" or len(splitted) > 2:
                raise botexceptions.InvalidBookmark(bookmark_name)
            elif len(splitted) == 1:
                playlist_id = None
            else:
                playlist_id = splitted[1].strip()
            self._controller.set_bookmark(bookmark_name, track_id, playlist_id)

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

    def _save_telegram(self):
        """
        Saves the telegram section
        """

        self._config.remove_section(self._telegram_section)
        self._config.add_section(self._telegram_section)
        self._config[self._telegram_section][self._telegram_entry_token] = self._telegram_token
        if self._controller.access:
            self._config[self._telegram_section][self._telegram_entry_users] = \
                ",".join(str(telegram_id) for telegram_id in self._controller.access)

    def _save_spotify(self):
        """

        Saves the spotify section
        """

        self._config.remove_section(self._spotify_section)
        self._config.add_section(self._spotify_section)
        self._config[self._spotify_section][self._spotify_entry_username] = self._spotify_username

    def _save_bookmarks(self):
        """

        Saves the bookmark section
        """

        if self._config.has_section(self._bookmark_section):
            self._config.remove_section(self._bookmark_section)
            self._config.add_section(self._bookmark_section)
            for bookmark in self._controller.get_bookmarks():
                track_id, playlist_id = self._controller.get_bookmark(bookmark)
                if playlist_id is None:
                    self._config[self._bookmark_section][bookmark] = track_id
                else:
                    self._config[self._bookmark_section][bookmark] = track_id + "," + playlist_id

    def save_config(self, configfile):
        """

        :param configfile: The file like object to write the config into
        :type configfile: File
        :return:
        :rtype:

        Write the config into the specified configfile
        """

        self._save_telegram()
        self._save_spotify()
        self._save_bookmarks()
        self._config.write(configfile)
        configfile.seek(0)
