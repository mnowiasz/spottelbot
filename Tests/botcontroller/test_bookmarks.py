import pytest

import botcontroller


# Add and remove bookmarks
class TestBookmarksAddRemove(object):
    _test_data = (
        # Bookmark name, title_id, playlist_id
        (botcontroller.bookmark_current, "12345", None),
        ("a", "6cdef0a", "abc12345"),
        ("mybookmark", "adef134", None),
        ("foo", "qras124dzu", "rerqzwe2")
    )

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        for entry in cls._test_data:
            name, title_id, playlist_id = entry
            cls._test_controller.set_bookmark(name, title_id, playlist_id)

    @pytest.mark.parametrize("bookmark_name, title_id, playlist_id", _test_data)
    def test_get_bookmark(self, bookmark_name, title_id, playlist_id):
        title, playlist = self._test_controller.get_bookmark(bookmark_name)
        assert title_id == title
        assert playlist_id == playlist

    # Clear all added bookmarks
    @pytest.mark.parametrize("bookmark_name, title_id, playlist_id", _test_data)
    def test_clear_bookmark(self, bookmark_name, title_id, playlist_id):
        self._test_controller.clear_bookmark(bookmark_name)
        with  pytest.raises(KeyError):
            title, playlist = self._test_controller.get_bookmark(bookmark_name)


# Misc tests
class TestBookmarkMisc(object):

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()

    # Test if a bookmark really gets overwritten
    def test_overwrite_bookmark(self):
        before = ("1234", "5678")
        after = ("abcd", None)
        bookmarkname = "footestoverride"
        self._test_controller.set_bookmark(bookmarkname, before[0], before[1])
        title, playlist = self._test_controller.get_bookmark(bookmarkname)

        assert (before[0], before[1]) == (title, playlist)

        self._test_controller.set_bookmark(bookmarkname, after[0], after[1])
        title, playlist = self._test_controller.get_bookmark(bookmarkname)

        assert (after[0], after[1]) == (title, playlist)

    # Access a nonexistent bookmark
    def test_nonexistent_bookmark(self):
        with  pytest.raises(KeyError):
            title, playlist = self._test_controller.get_bookmark("NONEXISTENT")

    # Clear a nonexistent bookmarks
    def test_clear_nonexistent_bookmark(self):
        with pytest.raises(KeyError):
            self._test_controller.clear_bookmark("NONEXISTENT")


# Sanitized Tests
class TestBookmarksSanitzied(object):
    _test_data = (
        ("    Test     ", "test"),
        ("Bookmark ", "bookmark"),
        ("A Bookmark Containing Spaces", "a_bookmark_containing_spaces"),
        ("   Combined Test    ", "combined_test"),
        ("\tTab\t", "tab")
    )

    _test_playlist = "TestProbe"

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        for entry in cls._test_data:
            name = entry[0]
            cls._test_controller.set_bookmark(name, name, cls._test_playlist)

    @pytest.mark.parametrize("name, sanitized", _test_data)
    def test_get_sanitzed_names(self, name, sanitized):
        title, playlist = self._test_controller.get_bookmark(sanitized)
        assert (name, self._test_playlist) == (name, playlist)

        title, playlist = self._test_controller.get_bookmark(name)
        assert (name, self._test_playlist) == (name, playlist)


    @pytest.mark.parametrize("name, sanitized", _test_data)
    def test_clear_sanitzied_names(self, name, sanitized):
        self._test_controller.clear_bookmark(name)
        with  pytest.raises(KeyError):
            title, playlist = self._test_controller.get_bookmark(sanitized)


# Test if the bookmarklist is sorted
class TestBookmarkSorted(object):
    _test_data = (
        ("Foxtrot", "Alpha", "Charlie", "Echo", "Delta", "Bravo", botcontroller.bookmark_current),
        [botcontroller.bookmark_current, "alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
    )

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        bookmarks = cls._test_data[0]
        for bookmark in bookmarks:
            cls._test_controller.set_bookmark(bookmark, None, None)  # Payload is unimportant

    def test_get_bookmarks(self):
        sorted_list = self._test_controller.get_bookmarks()
        assert self._test_data[1] == sorted_list
