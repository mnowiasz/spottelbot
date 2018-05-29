""" The Bot controller - access rights, bookmarks, and so on """
import botconfig
import spotifycontroller

bookmark_current = "Current"


# Make sure that "current" is first in list. After that, the list can be sorted
def _bookmark_compare(key):
    if key == bookmark_current:
        return " "
    else:
        return key


class BotController(object):

    botname = "MyBot"

    def __init__(self):
        self.access = set()
        self.bookmarks = {}
        self._translation_table = dict.fromkeys(map(ord, " \t"), "_")
        self.config = botconfig.BotConfig(self)
        self.spotify_controller = spotifycontroller.SpotifyController()

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

        Adds an entry to the list of allowed user ids. Raises a KeyError if the ID is already present
        """

        if self.has_access(telegram_id):
            raise KeyError(telegram_id)

        self.access.add(telegram_id)

    def remove_access(self, telegram_id: str):
        """

        :param telegram_id: the telegram ID
        :type telegram_id: str

        Removes the entry from the list of allowed user ids. Raises a KeyError if the ID is not present
        """

        self.access.remove(telegram_id)

    def clear_access(self):
        """

        Empties the access list/dictionary. Used in (re)loading the config
        """
        self.access = set()

    def _sanitize_bookmark(self, input: str) -> str:
        """

        :param input: The string to sanitize
        :type input: str
        :return: The sanitized string
        :rtype: str

        Removes trailing/leading spaces, and replaces certain characters (like spaces to underscores)
        """

        return input.strip().translate(self._translation_table)

    def set_bookmark(self, bookmark_name: str, track_id: str, playlist_id: str = None):
        """

        :param bookmark_name: The name of the bookmark ("current", "foo", "bar"..)
        :type bookmark_name: str
        :param track_id: Spotify's track ID - base62 coded
        :type track_id: str
        :param playlist_id: The (optional) playlist ID - base62 coded
        :type playlist_id: str

        Sets a bookmark. If already prsenet, the bookmark will be overwritten
        """
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
