""" The global config for the bot - users allowed to communicate, spotify token, ands so on"""


class Config(object):
    """ The global config object """
    botname = "MyBot"
    __access_set = set()

    def has_access(self, telegram_id: int)-> bool:
        """
        :param telegram_id: The telegram ID
        :type telegram_id: int
        :return: if the telegram ID is allowed to query the bot
        :rtype: bool

        Checks if the telgram ID is allowed to talk to the bot
        """
        return telegram_id in self.__access_set

    def add_access(self, telegram_id: int):
        """

        :param telegram_id: the telegram ID
        :type telegram_id: int

        Adds an entry to the list of allowed user ids. Raises a KeyError if the ID is already present
        """
        if self.has_access(telegram_id):
            raise KeyError(telegram_id)

        self.__access_set.add(telegram_id)

    def remove_access(self, telegram_id: int):
        """

        :param telegram_id: the telegram ID
        :type telegram_id: int

        Removes the entry from the list of allowed user ids. Raises a KeyError if the ID is not present
        """

        self.__access_set.remove(telegram_id)

