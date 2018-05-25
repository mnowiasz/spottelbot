import configparser
import os

import pytest

import botcontroller
import botexceptions

_config_path = os.path.dirname(os.path.realpath(__file__))
_config_file_valid = os.path.join(_config_path, "valid.config")
_controller = botcontroller.BotController()


def test_loadconfig():
    _controller.load_config(open(_config_file_valid))


@pytest.mark.parametrize("filename", ("missingsection1.config", "missingsection2.config"))
def test_loadconfig_missingsections(filename):
    config_file_missingsection = os.path.join(_config_path, filename)

    with pytest.raises(botexceptions.MissingSection):
        _controller.load_config(open(config_file_missingsection))


def test_telegram_token():
    _controller.load_config(open(_config_file_valid))
    assert "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" == _controller._telegram_token


def test_spotify_username():
    _controller.load_config(open(_config_file_valid))
    assert "SpotifyUser" == _controller._spotify_username


class TestAccessConfig(object):
    _test_data = (
        (12354, True),
        (543431, True),
        (4711, False)
    )

    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._controller.load_config(open(_config_file_valid))

    @pytest.mark.parametrize("telegram_id, access_granted", _test_data)
    def test_has_access(self, telegram_id, access_granted):
        assert access_granted == self._controller.has_access(telegram_id)


@pytest.mark.parametrize("filename", ("missingusers1.config", "missingusers2.config"))
def test_loadconfig_missingusers(filename):
    config_file_missingusers = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingUsers):
        _controller.load_config(open(config_file_missingusers))


def test_duplicate_users():
    config_file_duplicate = os.path.join(_config_path, "duplicateusers.config")
    with pytest.raises(botexceptions.DuplicateUsers) as duplicate:
        _controller.load_config(open(config_file_duplicate))
    assert 12354 == duplicate.value.duplicate_id


def test_loadconfig_badusers():
    config_file_badusers = os.path.join(_config_path, "badusers.config")
    with pytest.raises(botexceptions.InvalidUser) as invalid_exception:
        _controller.load_config(open(config_file_badusers))
    assert "bad_user" == invalid_exception.value.bad_id


@pytest.mark.parametrize("filename", ("missingtoken1.config", "missingtoken2.config"))
def test_loadconfig_missingtoken(filename):
    config_file_missingtoken = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingTelegramToken):
        _controller.load_config(open(config_file_missingtoken))


@pytest.mark.parametrize("filename", ("missingusername1.config", "missingusername2.config"))
def test_loadconfig_missingusername(filename):
    config_file_missingusername = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingSpotifyUsername):
        _controller.load_config(open(config_file_missingusername))


class TestBookmarks(object):
    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._controller.load_config(open(_config_file_valid))

    @pytest.mark.parametrize("bookmark_name, track_id, playlist_id", (
            ("current", "5aftzefdrefg", None),
            ("mybookmark", "zwdffee124455", "14r434343434"),
            ("alpha", "34q1341441414", "abcdef"),
            ("bravo", "xadf45342424", None)))
    def test_loadconfig_bookmarks(self, bookmark_name, track_id, playlist_id):
        assert (track_id, playlist_id) == self._controller.get_bookmark(bookmark_name)


def test_loadconfig_duplicatebookmarks():
    config_file_duplicate = os.path.join(_config_path, "duplicatebookmarks.config")
    with pytest.raises(configparser.DuplicateOptionError):
        _controller.load_config(open(config_file_duplicate))


def test_loadconfig_invalidbookmarks():
    config_file_invalid = os.path.join(_config_path, "invalidbookmarks.config")
    with pytest.raises(botexceptions.InvalidBookmark) as invalid_bookmark:
        _controller.load_config(open(config_file_invalid))
    assert "current" == invalid_bookmark.value.invalid_bookmark


def test_loadconfig_missingbookmarks():
    config_file_missing = os.path.join(_config_path, "missingbookmarks.config")
    with pytest.raises(botexceptions.InvalidBookmark) as invalid_bookmark:
        _controller.load_config(open(config_file_missing))
    assert "current" == invalid_bookmark.value.invalid_bookmark
