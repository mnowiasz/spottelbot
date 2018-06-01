""" Processing/relaying telegram messages"""
import botcontroller
import botexceptions
import spotifycontroller


def __parse_last_arg(parse_string):
    """

    :param parse_string: The string to parse
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
            lower_bound, upper_bound = __parse_last_arg(value)

    # /last with two arguments: /last 1- 5, /last 1 -5...
    elif len(arguments) == 2 or len(arguments) == 3:
        try:
            value = "".join(arguments)
            lower_bound, upper_bound = __parse_last_arg(value)
        except ValueError:
            raise botexceptions.InvalidRange(value)
    else:
        # Too much arguments
        raise botexceptions.InvalidRange(" ".join(arguments))

    if upper_bound < 1 or upper_bound > spotifycontroller.last_limit:
        raise botexceptions.InvalidRange(upper_bound)
    if lower_bound < 1 or lower_bound > spotifycontroller.last_limit:
        raise botexceptions.InvalidRange(lower_bound)

    return lower_bound, upper_bound


class TelegramDispatcher:

    def __init__(self, controller: botcontroller.BotController):
        self._controller = controller

    def mark(self, arguments: list):
        """

        :param arguments: Arguments to the "/mark" command
        :type arguments: list
        :return:
        :rtype:

        Sets a bookmark. Raises a InvalidBookmark exception if something is wrong
        """
        track_id = playlist_id = None
        bookmark_name = None
        index = -1

        if not arguments:
            # No arguments ("/mark")
            index = botcontroller.bookmark_current
            bookmark_name = botcontroller.bookmark_current

        elif len(arguments) == 1:
            # /mark with one argument (/mark current, /mark 5 == /mark current 5, /mark a == /mark a current
            value = arguments[0]

            if value.isdigit():
                # /mark 5, /mark 4
                index = int(value)
                bookmark_name = botcontroller.bookmark_current
            else:
                # /mark a, /mark current,,,
                if value == botcontroller.bookmark_current:
                    # /mark current
                    index = botcontroller.bookmark_current
                    bookmark_name = botcontroller.bookmark_current
                else:
                    # /mark a, /mark MyBookmark
                    index = botcontroller.bookmark_current
                    bookmark_name = value

        elif len(arguments) == 2:
            # /mark with two arguments - /mark current 5,/mark mybookmark current, /mark mybookmark 1
            bookmark_name = arguments[0]
            value = arguments[1]

            if value.isdigit():
                # /mark bookmark 5
                index = int(value)
            elif value == botcontroller.bookmark_current:
                index = botcontroller.bookmark_current
            else:
                # /mark bookmark something ?
                raise botexceptions.InvalidBookmark(value)
        else:
            # More than 2 arguments - /mark bookmark 5 3 4. Makes no sense
            raise botexceptions.InvalidBookmark(" ".join(arguments))

        if index == bookmark_name:
            (track_id, playlist_id) = self._controller.spotify_controller.get_current()
        else:
            (track_id, playlist_id) = self._controller.spotify_controller.get_last_index(index)
        self._controller.set_bookmark(bookmark_name, track_id, playlist_id)

    def delete(self, arguments: list):
        """

        :param arguments: The arguments given to the "/delete" command
        :type arguments: list
        :return:
        :rtype:

        Deletes a (or some) bookmark(s) (or all, /delete or /clear all), Raises an invalid bookmark exception.
        """

        # /delete without an argument
        if arguments is None:
            raise botexceptions.InvalidBookmark("<none>")

        for argument in arguments:
            # /delete 5
            if argument.isdigit():
                raise botexceptions.InvalidBookmark(argument)
            elif argument == botcontroller.bookmark_all:
                self._controller.clear_bookmarks()
                break  # No point in going on. All bookmars are deleted.
            else:
                self._controller.clear_bookmark(argument)
