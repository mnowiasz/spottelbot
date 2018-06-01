""" The Bot controller - access rights, bookmarks, and so on """
import botconfig
import botexceptions
import spotifycontroller

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

    def _sanitize_bookmark(self, input: str) -> str:
        """

        :param input: The string to sanitize
        :type input: str
        :return: The sanitized string
        :rtype: str

        Removes trailing/leading spaces, and replaces certain characters (like spaces to underscores). Also transforms
        to lower
        """

        return input.strip().translate(self._translation_table).lower()

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
