import botconfig
import pytest


def test_botname():
    test_config = botconfig.Config()
    assert test_config.botname == "MyBot"


class TestAcess(object):
    _test_data = (
        # ID, Access granted, exception raised (add)
        (1, True, False),
        (2, False, False),
        (3, True, False),
        (4, True, False),
        (4, True, True),
        (1, True, True)
    )

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.Config()
        for item in cls._test_data:
            telegram_id, access_granted, exception_expected = item
            if access_granted:
                if exception_expected:
                    with pytest.raises(KeyError):
                        cls._test_config.add_access(telegram_id)
                else:
                    cls._test_config.add_access(telegram_id)

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_has_access(self, telegram_id, access_granted, exception_expected):
        if exception_expected:
            pass
        assert self._test_config.has_access(telegram_id) == access_granted

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_remove_access(self, telegram_id, access_granted, exception_expected):
        # If an exception was expected the duplicate ID wasn't added. However, the original ID was added
        if exception_expected:
            pass
        elif not access_granted:
            with  pytest.raises(KeyError):
                self._test_config.remove_access(telegram_id)
        else:
            self._test_config.remove_access(telegram_id)
            assert not self._test_config.has_access(telegram_id)


class TestBookmarks(object):
    _test_data = (
        # Bookmark name, title_id, playlist_id
        ("current", "12345", None),
        ("A", "6cdef0a", "abc12345"),
        ("MyBookmark", "adef134", None),
        ("Foo", "qras124dzu", "rerqzwe2")
    )

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.Config()
        for entry in cls._test_data:
            name, title_id, playlist_id = entry
            cls._test_config.set_bookmark(name, title_id, playlist_id)

    @pytest.mark.parametrize("bookmark_name, title_id, playlist_id", _test_data)
    def test_get_bookmark(self, bookmark_name, title_id, playlist_id):
        title, playlist = self._test_config.get_bookmark(bookmark_name)
        assert title == title_id
        assert playlist == playlist_id

    # Test if a bookmark really gets overwritten
    def test_overwrite_bookmark(self):
        before = ("1234", "5678")
        after = ("abcd", None)
        bookmarkname = "FooTestOverride"
        self._test_config.set_bookmark(bookmarkname, before[0], before[1])
        title, playlist = self._test_config.get_bookmark(bookmarkname)

        assert title == before[0]
        assert playlist == before[1]

        self._test_config.set_bookmark(bookmarkname, after[0], after[1])
        title, playlist = self._test_config.get_bookmark(bookmarkname)

        assert title == after[0]
        assert playlist == after[1]

    def test_nonexistent_bookmark(self):
        with  pytest.raises(KeyError):
            title, playlist = self._test_config.get_bookmark("NONEXISTENT")

    def test_clear_nonexistent_bookmkar(self):
        with pytest.raises(KeyError):
            self._test_config.clear_bookmark("NONEXISTENT")

    @pytest.mark.parametrize("bookmark_name, title_id, playlist_id", _test_data)
    def test_clear_bookmark(self, bookmark_name, title_id, playlist_id):
        self._test_config.clear_bookmark(bookmark_name)
        with  pytest.raises(KeyError):
            title, playlist = self._test_config.get_bookmark(bookmark_name)
