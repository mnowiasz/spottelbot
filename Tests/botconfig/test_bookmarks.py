import pytest

import botconfig


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
