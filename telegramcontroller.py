""" Processing/relaying telegram messages"""
import collections
import threading

import telegram
import telegram.bot
import telegram.ext

import botconfig
import botexceptions
import spotifycontroller

max_message_length = 4096


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

    if value_list[1] == "":
        upper_bound = spotifycontroller.last_limit
    else:
        upper_bound = int(value_list[1])

    return lower_bound, upper_bound


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


class TelegramController(object):
    class Decorators(object):
        @classmethod
        def restricted(self, method):
            def wrapper(self, bot: telegram.Bot, update: telegram.Update, args):
                user: telegram.User = update.message.from_user
                if self._config.has_access("@" + user.username) or self._config.has_access(user.id):
                    return method(self, bot, update, args)
                else:
                    return self._unauthorized(bot, update, args)

            return wrapper

        @classmethod
        def autosave(self, method):
            def wrapper(self, *args, **kwargs):
                # TODO: Autosave on/off

                retval = method(self, *args, **kwargs)
                self._config.save_config(None)
                return retval

            return wrapper

    def __init__(self, config: botconfig.BotConfig, spotify_controller: spotifycontroller.SpotifyController):
        """

        :param config: The botconfig
        :type config: botconfig.BotConfig
        :param spotify_controller: spotify controller
        :type spotify_controller: spotifycontroller.SpotifyController
        """
        self._config = config
        self._spotify_controller = spotify_controller
        self._updater = None
        self._output_buffer = ""

        # Command(s), handler, Helptext
        self._handlers = (
            (("bye", "quit", "shutdown"), self._quit_handler, "Shutdown the bot (caution!)"),
            ("whoami", self._whoami_handler, "Shows the Username and it's numeric ID"),
            ("help", self._help_handler, "This command"),
            ("current", self._current_handler, "Get the currently playing track"),
            ("last", self._last_handler, "Recently played tracks"),
            (("show", "list"), self._list_handler, "Shows the bookmark(s)"),
            (("mark", "set"), self._mark_handler, "Sets a bookmark"),
            (("clear", "delete"), self._clear_handler, "Deletes bookmark(s) (or all)")
        )

    def _send_message_buffer(self, bot: telegram.Bot, chat_id: str, text: str, final=False, **kwargs):
        """

        :param bot: Telegram bot
        :type bot: telegram.Bot
        :param chat_id: Chat ID to send the messages to
        :type chat_id: str
        :param text: The text to send
        :type text: str
        :param final: Last part of the message, i.e. flush the buffer?
        :type final: bool
        :param kwargs: args to pass to bot.send_message()
        :type kwargs:
        :return:
        :rtype:

        Sends a bunch of message lines to the chat_id, honoring telegram's max message length. If a single line
        (text) should exceed the maximum message length, an exception will be raised
        """

        # Not sure if there should be a seperate buffer for eatch chat_id.. i.e. is this method thread safe? Does
        # it need to be? For know there won't be buffers per chat_id, only one single, global one.

        message_length = len(text)

        if message_length >= max_message_length:
            raise botexceptions.TelegramMessageLength(message_length)

        if len(self._output_buffer) + message_length >= max_message_length:
            bot.send_message(chat_id=chat_id, text=self._output_buffer, **kwargs)
            self._output_buffer = text
        else:
            self._output_buffer += text

        # There's no case final is set and there's an empty buffer: If buffer is full, buffer contains the
        # message containing the potential overflow.
        if final:
            bot.send_message(chat_id=chat_id, text=self._output_buffer, **kwargs)
            self._output_buffer = ""

    def connect(self):
        """

        :return:
        :rtype:

        Connect to telegram, start the loop
        """
        self._updater = telegram.ext.Updater(self._config.telegram_token)

        for handler in self._handlers:
            command_s = handler[0]
            method_handler = handler[1]
            if isinstance(command_s, collections.Iterable) and not isinstance(command_s, str):
                for command in command_s:
                    self._updater.dispatcher.add_handler(
                        telegram.ext.CommandHandler(command, method_handler, pass_args=True))
            else:
                self._updater.dispatcher.add_handler(
                    telegram.ext.CommandHandler(command_s, method_handler, pass_args=True))

        self._updater.start_polling()

    def _unauthorized(self, bot: telegram.Bot, update: telegram.Update, args):
        bot.send_message(chat_id=update.message.chat_id, text="You are not authorized to use this function")

    # "/whoami"
    def _whoami_handler(self, bot: telegram.Bot, update: telegram.Update, args):

        user: telegram.User = update.message.from_user
        message = "You are @{} ({})".format(user.username, user.id)
        bot.send_message(chat_id=update.message.chat_id, text=message)

    # Has to be called from another thread
    def _quit(self):
        self._updater.stop()
        self._updater.is_idle = False

    # /quit, /shutdown, bye
    @Decorators.restricted
    def _quit_handler(self, bot: telegram.Bot, update: telegram.Update, args):
        bot.send_message(chat_id=update.message.chat_id, text="Shutting down")
        threading.Thread(target=self._quit).start()

    def _help_handler(self, bot: telegram.Bot, update: telegram.Update, args):
        bot.send_message(chat_id=update.message.chat_id, text="Help!")

    def _current_handler(self, bot: telegram.Bot, update: telegram.Update, args):
        message = self._spotify_controller.get_current()
        if not message:
            message = "Nothing playing at the moment"

        bot.send_message(chat_id=update.message.chat_id, text=message)

    # /last
    @Decorators.restricted
    def _last_handler(self, bot: telegram.Bot, update: telegram.Update, args):

        output = ""

        try:
            lower, upper = _last_range(args)
            output_list = self._spotify_controller.get_last_tracks(lower, upper)

            for i, item in enumerate(output_list, lower):
                text = "*{}*: {}\n".format(i, item)
                self._send_message_buffer(bot, update.message.chat_id, text=text, final=False,
                                          parse_mode=telegram.ParseMode.MARKDOWN)
            self._send_message_buffer(bot, update.message.chat_id, text="", final=True,
                                      parse_mode=telegram.ParseMode.MARKDOWN)
        except botexceptions.InvalidRange as range_error:
            output = "Invalid range {}. Must be between 1 and {}".format(range_error.invalid_argument,
                                                                         spotifycontroller.last_limit)

    # /list, /show
    @Decorators.restricted
    def _list_handler(self, bot: telegram.Bot, update: telegram.Update, args):

        # 1.) /list without any argument -> list all bookmarks
        if len(args) == 0:
            bookmark_list = self._config.get_bookmarks()
            if bookmark_list:
                text = ""
                for bookmark in bookmark_list:
                    track_id, playlist_id = self._config.get_bookmark(bookmark)
                    text = "*{}*: {}".format(bookmark, self._spotify_controller.get_track(track_id))
                    if playlist_id:
                        text += " (Playlist {})".format(self._spotify_controller.get_playlist(playlist_id))
                    text += "\n"
                    self._send_message_buffer(bot, update.message.chat_id, text=text, final=False,
                                              parse_mode=telegram.ParseMode.MARKDOWN)
                self._send_message_buffer(bot, update.message.chat_id, text=text, final=True,
                                          parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                self._send_message_buffer(bot, update.message.chat_id, text="Not bookmars found", final=True,
                                          parse_mode=telegram.ParseMode.MARKDOWN)

    # /mark, /set..
    @Decorators.restricted
    @Decorators.autosave
    def _mark_handler(self, bot: telegram.Bot, update: telegram.Update, args):
        message = self.mark(args)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        # TODO: Exception

    # /clear, /delete...
    @Decorators.restricted
    @Decorators.autosave
    def _clear_handler(self, bot: telegram.Bot, update: telegram.Update, args):

        message = ""
        try:
            message = self.delete(args)
        except botexceptions.InvalidBookmark as invalid:
            message = "Invalid bookmark name {}".format(invalid.invalid_bookmark)

        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

    def mark(self, arguments: list) -> str:
        """

        :param arguments: Arguments to the "/mark" command
        :type arguments: list
        :return: Outputsting ("Marked", "currently nothing playing")
        :rtype: str

        Sets a bookmark. Raises a InvalidBookmark exception if something is wrong
        """
        track_id = playlist_id = None
        bookmark_name = None
        index = -1

        if not arguments:
            # No arguments ("/mark")
            index = botconfig.bookmark_current
            bookmark_name = botconfig.bookmark_current

        elif len(arguments) == 1:
            # /mark with one argument (/mark current, /mark 5 == /mark current 5, /mark a == /mark a current
            value = arguments[0]

            if value.isdigit():
                # /mark 5, /mark 4
                index = int(value)
                bookmark_name = botconfig.bookmark_current
            else:
                # /mark a, /mark current,,,
                if value == botconfig.bookmark_current:
                    # /mark current
                    index = botconfig.bookmark_current
                    bookmark_name = botconfig.bookmark_current
                else:
                    # /mark a, /mark MyBookmark
                    index = botconfig.bookmark_current
                    bookmark_name = value

        elif len(arguments) == 2:
            # /mark with two arguments - /mark current 5,/mark mybookmark current, /mark mybookmark 1
            bookmark_name = arguments[0]
            value = arguments[1]

            if value.isdigit():
                # /mark bookmark 5
                index = int(value)
            elif value == botconfig.bookmark_current:
                index = botconfig.bookmark_current
            else:
                # /mark bookmark something ?
                raise botexceptions.InvalidBookmark(value)
        else:
            # More than 2 arguments - /mark bookmark 5 3 4. Makes no sense
            raise botexceptions.InvalidBookmark(" ".join(arguments))

        if index == bookmark_name or index == botconfig.bookmark_current:
            (track_id, playlist_id) = self._spotify_controller.get_current(formatted=False)
            if not track_id:
                return "Cannot set bookmark: Nothing playing right now"
        else:
            (track_id, playlist_id) = self._spotify_controller.get_last_index(index)

        self._config.set_bookmark(bookmark_name, track_id, playlist_id)
        return "Bookmark {} set".format(bookmark_name)

    def delete(self, arguments: list) -> str:
        """

        :param arguments: The arguments given to the "/delete" command
        :type arguments: list
        :return: output of command
        :rtype: str

        Deletes a (or some) bookmark(s) (or all, /delete or /clear all), Raises an InvalidBookmarkException/UnknownBookmarkException
        """
        output = ""
        # /delete without an argument
        if arguments is None:
            raise botexceptions.InvalidBookmark("<none>")

        for argument in arguments:

            if argument == botconfig.bookmark_all:
                self._config.clear_bookmarks()
                output = "*All bookmarks have been cleared*"
                break  # No point in going on. All bookmarks are deleted.

            try:
                self.delete_single(argument)
                output += "{} has been deleted\n".format(argument)
            except botexceptions.InvalidBookmark as invalid:
                output += "Invalid bookmark {}\n".format(argument)
            except KeyError:
                output += "Unknown bookmark {}\n".format(argument)

        return output

    def delete_single(self, bookmark_name: str):
        """

        :param bookmark_name: Name of the bookmark. Raises InvalidBookmark if illegal
        :type bookmark_name: str
        :return:
        :rtype:
        """

        if not bookmark_name:
            raise botexceptions.InvalidBookmark("<none>")
        if bookmark_name.isdigit():
            raise botexceptions.InvalidBookmark(bookmark_name)
        self._config.clear_bookmark(bookmark_name)

    def deluser(self, telegram_ids):
        """

        :param telegram_ids: The arguments given to the "/deluser" command
        :type telegram_ids: list
        :return:
        :rtype:

        Removes access for one (or multiple) users. Raises the usual exceptions
        """

        for single_id in telegram_ids:
            self._config.remove_access(single_id)

    def adduser(self, telegram_ids):
        """

        :param telegram_ids: The arguments given to the /adduser command
        :type telegram_ids: list
        :return:
        :rtype:

        Adds access for one (or multiple) users. Raises the usual exceptions
        """

        for single_id in telegram_ids:
            self._config.add_access(single_id)
