import configparser
import os

import pytest

from spottelbot import botexceptions, botconfig

_config_path = os.path.dirname(os.path.realpath(__file__))
_config_file_valid = os.path.join(_config_path, "valid.config")
_config = botconfig.BotConfig()


def test_loadconfig():
    _config.load_config(_config_file_valid)


@pytest.mark.parametrize("filename", ("missingsection1.config", "missingsection2.config"))
def test_loadconfig_missingsections(filename):
    config_file_missingsection = os.path.join(_config_path, filename)

    with pytest.raises(botexceptions.MissingSection):
        _config.load_config(config_file_missingsection)


def test_telegram_token():
    _config.load_config(_config_file_valid)
    assert "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw" == _config.telegram_token


def test_spotify_username():
    _config.load_config(_config_file_valid)
    assert "SpotifyUser" == _config._spotify_username


def test_spotify_client_id():
    _config.load_config(_config_file_valid)
    assert "avcdeefg" == _config._spotify_client_id


def test_spotify_client_secret():
    _config.load_config(_config_file_valid)
    assert "12345t6343" == _config._spotify_client_secret


def test_spotify_redirect_uri():
    _config.load_config(_config_file_valid)
    assert "http://localhost/xyz" == _config._spotify_redirect_uri


class TestAccessConfig(object):
    _test_data = (
        ("12354", True),
        ("543431", True),
        ("4711", False),
        ("@myaccount", True),
        ("@anotheruser", True),
        ("@nosuchuser", False)
    )

    @classmethod
    def setup_class(cls):
        cls._config = botconfig.BotConfig()
        cls._config.load_config(_config_file_valid)

    @pytest.mark.parametrize("telegram_id, access_granted", _test_data)
    def test_has_access(self, telegram_id, access_granted):
        assert access_granted == self._config.has_access(telegram_id)


@pytest.mark.parametrize("filename", ("missingusers1.config", "missingusers2.config"))
def test_loadconfig_missingusers(filename):
    config_file_missingusers = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingUsers):
        _config.load_config(config_file_missingusers)


def test_duplicate_users():
    config_file_duplicate = os.path.join(_config_path, "duplicateusers.config")
    with pytest.raises(botexceptions.DuplicateUsers) as duplicate:
        _config.load_config(config_file_duplicate)
    assert "12354" == duplicate.value.duplicate_id


def test_loadconfig_badusers():
    config_file_badusers = os.path.join(_config_path, "badusers.config")
    with pytest.raises(botexceptions.InvalidUser) as invalid_exception:
        _config.load_config(config_file_badusers)
    assert "bad_user" == invalid_exception.value.bad_id


@pytest.mark.parametrize("filename", ("missingtoken1.config", "missingtoken2.config"))
def test_loadconfig_missingtoken(filename):
    config_file_missingtoken = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingTelegramToken):
        _config.load_config(config_file_missingtoken)


@pytest.mark.parametrize("filename", ("missingusername1.config", "missingusername2.config"))
def test_loadconfig_missingusername(filename):
    config_file_missingusername = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingSpotifyUsername):
        _config.load_config(config_file_missingusername)


class TestBookmarks(object):
    @classmethod
    def setup_class(cls):
        cls._config = botconfig.BotConfig()
        cls._config.load_config(_config_file_valid)

    @pytest.mark.parametrize("bookmark_name, track_id, playlist_id", (
            ("current", "5aftzefdrefg", None),
            ("mybookmark", "zwdffee124455", "14r434343434"),
            ("alpha", "34q1341441414", "abcdef"),
            ("bravo", "xadf45342424", None)))
    def test_loadconfig_bookmarks(self, bookmark_name, track_id, playlist_id):
        assert (track_id, playlist_id) == self._config.get_bookmark(bookmark_name)


def test_loadconfig_duplicatebookmarks():
    config_file_duplicate = os.path.join(_config_path, "duplicatebookmarks.config")
    with pytest.raises(configparser.DuplicateOptionError):
        _config.load_config(config_file_duplicate)


def test_loadconfig_invalidbookmarks():
    config_file_invalid = os.path.join(_config_path, "invalidbookmarks.config")
    with pytest.raises(botexceptions.InvalidBookmark) as invalid_bookmark:
        _config.load_config(config_file_invalid)
    assert "current" == invalid_bookmark.value.invalid_bookmark


def test_loadconfig_missingbookmarks():
    config_file_missing = os.path.join(_config_path, "missingbookmarks.config")
    with pytest.raises(botexceptions.InvalidBookmark) as invalid_bookmark:
        _config.load_config(config_file_missing)
    assert "current" == invalid_bookmark.value.invalid_bookmark


def test_duplicate_configread():
    _config.load_config(_config_file_valid)
    _config.load_config(_config_file_valid)
    _config.load_config(_config_file_valid)
