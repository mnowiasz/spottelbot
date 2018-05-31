""" Tests of the mark / bookmark features"""
import random
import string

import pytest

import botcontroller
import botexceptions
import spotifycontroller
import telegramdispatcher

""" Mock track ids"""


def _random_id():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=16))


_current_id = (_random_id(), _random_id())

_mock_tracks = [(_random_id(), _random_id()) for i in range(0, spotifycontroller.last_limit)]


def mockget_current():
    return _current_id


def mockget_last_index(last_id):
    if last_id == botcontroller.bookmark_current:
        return mockget_current()
    else:
        return _mock_tracks[last_id]

# /mark without any parameter
def test_mark_current(monkeypatch):
    controller = botcontroller.BotController()

    dispatcher = telegramdispatcher.TelegramDispatcher(controller)

    monkeypatch.setattr(controller.spotify_controller, "get_current", mockget_current)

    dispatcher.mark(None)

    assert mockget_current() == controller.get_bookmark(botcontroller.bookmark_current)


class TestMark:

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        cls._test_dispatcher = telegramdispatcher.TelegramDispatcher(cls._test_controller)

    # /mark with parameters
    @pytest.mark.parametrize("params, bookmark_name, bookmark_index, exception_expected", (
            ([botcontroller.bookmark_current], botcontroller.bookmark_current, botcontroller.bookmark_current, False),
            (["Bookmark"], "bookmark", botcontroller.bookmark_current, False),
            (["A", botcontroller.bookmark_current], "a", botcontroller.bookmark_current, False),
            (["MyBookmark", "5"], "mybookmark", 5, False),
            (["A", "B", "5"], None, None, True),
            (["bookmark", str(spotifycontroller.last_limit + 1)], None, None, True),
            ([botcontroller.bookmark_current, "9"], botcontroller.bookmark_current, 9, False)
    ))
    def test_mark(self, monkeypatch, params, bookmark_name, bookmark_index, exception_expected):
        monkeypatch.setattr(self._test_controller.spotify_controller, "get_current", mockget_current)
        monkeypatch.setattr(self._test_controller.spotify_controller, "get_last_index", mockget_last_index)

        if exception_expected:
            with pytest.raises((botexceptions.InvalidBookmark, IndexError)):
                self._test_dispatcher.mark(params)
        else:
            self._test_dispatcher.mark(params)
            assert mockget_last_index(bookmark_index) == self._test_controller.get_bookmark(bookmark_name)
