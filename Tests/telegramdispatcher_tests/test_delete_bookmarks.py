""" Test /delete commands"""

import pytest

import botcontroller
import botexceptions
import telegramdispatcher


class TestDeleteBookmarks(object):
    _test_data = (
        # Bookmark name, title_id, playlist_id
        (botcontroller.bookmark_current, "12345", None),
        ("a", "6cdef0a", "abc12345"),
        ("mybookmark", "adef134", None),
        ("foo", "qras124dzu", "rerqzwe2"))

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        cls._test_dispatcher = telegramdispatcher.TelegramDispatcher(cls._test_controller)

        for entry in cls._test_data:
            name, title_id, playlist_id = entry
            cls._test_controller.set_bookmark(name, title_id, playlist_id)

    @pytest.mark.parametrize("params, bookmark_name, exception_expected", (
            (None, None, True),
    ))
    def test_delete_bookmark(self, params, bookmark_name, exception_expected):
        if exception_expected:
            with pytest.raises(botexceptions.InvalidBookmark):
                self._test_dispatcher.delete(params)
