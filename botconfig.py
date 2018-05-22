""" The global config for the bot - users allowed to communicate, spotify token, ands so on"""

bookmark_current = "Current"


class Config(object):
    """ The global config object """
    botname = "MyBot"

    def __init__(self):
        self.__access = set()
        self.__bookmarks = {}
        self._translation_table = dict.fromkeys(map(ord, " \t"), "_")

    def has_access(self, telegram_id: int) -> bool:
        """
        :param telegram_id: The telegram ID
        :type telegram_id: int
        :return: if the telegram ID is allowed to query the bot
        :rtype: bool

        Checks if the telgram ID is allowed to talk to the bot
        """
        return telegram_id in self.__access

    def add_access(self, telegram_id: int):
        """

        :param telegram_id: the telegram ID
        :type telegram_id: int

        Adds an entry to the list of allowed user ids. Raises a KeyError if the ID is already present
        """
        if self.has_access(telegram_id):
            raise KeyError(telegram_id)

        self.__access.add(telegram_id)

    def remove_access(self, telegram_id: int):
        """

        :param telegram_id: the telegram ID
        :type telegram_id: int

        Removes the entry from the list of allowed user ids. Raises a KeyError if the ID is not present
        """

        self.__access.remove(telegram_id)

    def _sanitize_bookmark(self, input: str) -> str:
        """

        :param input: The string to sanitize
        :type input: str
        :return: The sanitized string
        :rtype: str

        Removes trailing/leading spaces, and replaces certain characters (like spaces to underscores)
        """

        return input.strip().translate(self._translation_table)



    def set_bookmark(self, bookmark_name: str, title_id: str, playlist_id: str = None):
        """

        :param bookmark_name: The name of the bookmark ("current", "foo", "bar"..)
        :type bookmark_name: str
        :param title_id: Spotify's title ID - base62 coded
        :type title_id: str
        :param playlist_id: The (optional) playlist ID - base62 coded
        :type playlist_id: str

        Sets a bookmark. If already prsenet, the bookmark will be overwritten
        """
        self.__bookmarks[self._sanitize_bookmark(bookmark_name)] = (title_id, playlist_id)

    def get_bookmark(self, bookmark_name: str) -> (str, str):
        """

        :param bookmark_name: The name of the bookmark ("current", "a")
        :type bookmark_name: str
        :return: The ID of the title and (optionally) playlist
        :rtype: (str, str)

        Gets a bookmark. If the name of the bookmark doesn't exist a KeyError will be raised
        """
        return self.__bookmarks[self._sanitize_bookmark(bookmark_name)]

    def clear_bookmark(self, bookmark_name: str):
        """

        :param bookmark_name: The name of the bookmark ("current", "a")
        :type bookmark_name: str

        Clears the bookmark. If the bookmark doesn't exist a KeyError will be raised
        """

        del self.__bookmarks[self._sanitize_bookmark(bookmark_name)]

    # Make sure that "current" is first in list. After that, the list can be sorted
    def _bookmark_compare(self, key):
        if key == bookmark_current:
            return " "
        else:
            return key

    def get_bookmarks(self) -> list:
        """

        :return The sorted list of bookmarks
        :rtype list
        Returns the name of the bookmarks in a sorteds list, with "current" as the first entry
        """
        return sorted(self.__bookmarks.keys(), key=self._bookmark_compare)
