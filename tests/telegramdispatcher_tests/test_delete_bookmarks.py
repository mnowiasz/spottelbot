""" Test /delete commands"""

import pytest

import botconfig
import botexceptions
from tests.testdata import TestBookmarkData


# /delete with a single argument
class TestDeleteBookmarkSingle(TestBookmarkData):

    @pytest.mark.parametrize("params, bookmark_name, exception_expected", (
            (None, None, True),
            (str(botconfig.bookmark_current), (botconfig.bookmark_current), False),
            ("mybookmark", ("mybookmark"), False),
            ("5", None, True)
    ))
    def test_delete_bookmark_single(self, params, bookmark_name, exception_expected):
        if exception_expected:
            with pytest.raises(botexceptions.InvalidBookmark):
                self._test_dispatcher.delete_single(params)
        else:
            self._test_dispatcher.delete_single(params)
            with pytest.raises(KeyError):
                self._test_config.get_bookmark(bookmark_name)


# /delete all
class TestDeleteAll(TestBookmarkData):

    def test_delete_bookmark_all(self):
        self._test_dispatcher.delete([botconfig.bookmark_all])
        assert 0 == len(self._test_config.bookmarks)
