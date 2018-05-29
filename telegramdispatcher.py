""" Processing/relaying telegram messages"""
import botcontroller
import botexceptions
import spotifycontroller


def __parse_arg(parse_string):
    """

    :param parse_string: The string ti oarse
    :type parse_string: str
    :return: A tuple containung upper and lower bound
    :rtype: tuple

    Parses arguments like "1-5", "1-".
    """

    lower_bound = upper_bound = 0
    value_list = parse_string.split('-')

    # No "-" in the value
    if len(value_list) == 1:
        raise botexceptions.InvalidRange(parse_string)

    # "-value"
    if value_list[0] == "":

        # Edge Case: "-5-6" (negative value as first argument)
        if len(value_list) != 2:
            raise botexceptions.InvalidRange(parse_string)
        lower_bound = 1
    else:
        lower_bound = int(value_list[0])
    upper_bound = int(value_list[1])

    return (lower_bound, upper_bound)


def _last_range(arguments):
    """

    :param arguments: List of arguments given to "/last"
    :type arguments: list
    :return: uper and lower bound
    :rtype: tuple

    Converts the argument to "/last" to a tuple (lower boundary, upper boundary). Throws InvalidRange execption if
    the arguments are out of bounds or are invalid
    """
    lower_bound = upper_bound = 0

    # Empty argument ("/last")
    if not arguments:
        lower_bound = 1
        upper_bound = spotifycontroller.last_limit

    # "/last with one argument.
    elif len(arguments) == 1:

        value = arguments[0]

        # Case 1: /last with exactly one numeric argument (/last 5)
        if value.isdigit():
            lower_bound = 1
            upper_bound = int(arguments[0])
        else:
            # Case 2: /last with a ranged argument (/last 1-5, /last 5-, /last -10
            lower_bound, upper_bound = __parse_arg(value)

    # /last with two arguments: /last 1- 5, /last 1 -5...
    elif len(arguments) == 2 or len(arguments) == 3:
        try:
            value = ""
            for string in arguments:
                value += string
            lower_bound, upper_bound = __parse_arg(value)
        except ValueError:
            raise botexceptions.InvalidRange(value)
    else:
        # Too much arguments
        invalid_value = ""
        for string in arguments:
            invalid_value += string
            raise botexceptions.InvalidRange(invalid_value)

    if upper_bound < 1 or upper_bound > spotifycontroller.last_limit:
        raise botexceptions.InvalidRange(upper_bound)
    if lower_bound < 1 or lower_bound > spotifycontroller.last_limit:
        raise botexceptions.InvalidRange(lower_bound)

    return (lower_bound, upper_bound)


class TelegramDispatcher:

    def __init__(self, controller: botcontroller.BotController):
        self._controller = controller

    def mark(self, arguments):
        """

        :param arguments: Arguments to the "/mark" command
        :type arguments: list
        :return:
        :rtype:

        Sets a bookmark
        """

        (track_id, playlist_id) = self._controller.spotify_controller.get_current()
        self._controller.set_bookmark(botcontroller.bookmark_current, track_id, playlist_id)
