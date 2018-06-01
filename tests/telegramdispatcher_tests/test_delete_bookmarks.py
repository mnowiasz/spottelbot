""" Test /delete commands"""

import pytest

import botcontroller
import botexceptions
from tests.testdata import TestBookmarkData


# /delete with a single argument
class TestDeleteBookmarkSingle(TestBookmarkData):

    @pytest.mark.parametrize("params, bookmark_name, exception_expected", (
            (None, None, True),
            ([str(botcontroller.bookmark_current)], (botcontroller.bookmark_current), False),
            (["mybookmark"], ("mybookmark"), False),
            (["5"], None, True)
    ))
    def test_delete_bookmark_single(self, params, bookmark_name, exception_expected):
        if exception_expected:
            with pytest.raises(botexceptions.InvalidBookmark):
                self._test_dispatcher.delete(params)
        else:
            self._test_dispatcher.delete(params)
            with pytest.raises(KeyError):
                self._test_controller.get_bookmark(bookmark_name)


# /delete with multiple arguments
class TestDeleteBookmarkMultiple(TestBookmarkData):

    @pytest.mark.parametrize("params, bookmarks, exception_expected", (
            (["5", "a"], None, True),
            (["a", "5"], None, True),
            # Side effect: "a" has been deleted before the exception concerning "5", so "a" cannot be used anymore
            (["mybookmark", "foo", "bar"], ("mybookmark", "foo", "bar"), False)
    ))
    def test_delete_bookmark_multiple(self, params, bookmarks, exception_expected):
        if exception_expected:
            with pytest.raises(botexceptions.InvalidBookmark):
                self._test_dispatcher.delete(params)
        else:
            self._test_dispatcher.delete(params)
            for bookmark in bookmarks:
                with pytest.raises(KeyError):
                    self._test_controller.get_bookmark(bookmark)


# /delete all
class TestDeleteAll(TestBookmarkData):

    def test_delete_bookmark_all(self):
        self._test_dispatcher.delete([botcontroller.bookmark_all])
        assert 0 == len(self._test_controller.bookmarks)
