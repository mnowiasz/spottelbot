"""Test data to share - do not repeat yourself"""

import pytest

import botconfig
import telegramdispatcher


# Test data for access
class TestAccessData(object):
    _test_data = (
        # ID, Access granted, exception raised (add)
        ("1", True, False),
        ("2", False, False),
        ("3", True, False),
        ("4", True, False),
        ("4", True, True),
        ("1", True, True),
        ("@myaccount", True, False),
        ("@anotheruser", True, False)
    )

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.BotConfig()
        for item in cls._test_data:
            telegram_id, access_granted, exception_expected = item
            if access_granted:
                if exception_expected:
                    with pytest.raises(KeyError):
                        cls._test_config.add_access(telegram_id)
                else:
                    cls._test_config.add_access(telegram_id)


# Adding/Removing Bookmarks

class TestBookmarkData(object):
    _test_data = (
        # Bookmark name, title_id, playlist_id
        (botconfig.bookmark_current, "12345", None),
        ("a", "6cdef0a", "abc12345"),
        ("mybookmark", "adef134", None),
        ("foo", "qras124dzu", "rerqzwe2"),
        ("bar", "awrrfaadeaa", None)
    )

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.BotConfig()
        cls._test_dispatcher = telegramdispatcher.TelegramDispatcher(cls._test_config, None)

        for entry in cls._test_data:
            name, title_id, playlist_id = entry
            cls._test_config.set_bookmark(name, title_id, playlist_id)
