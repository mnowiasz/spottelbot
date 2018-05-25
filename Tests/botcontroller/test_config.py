import configparser
import os

import pytest

import botcontroller
import botexceptions

_config_path = os.path.dirname(os.path.realpath(__file__))
_config_file_valid = os.path.join(_config_path, "valid.config")
_controller = botcontroller.BotController()


def test_loadconfig_nonexistent():
    with  pytest.raises(FileNotFoundError):
        _controller.load_config("broken.config")


def test_loadconfig():
    _controller.load_config(_config_file_valid)


@pytest.mark.parametrize("filename", ("missingsection1.config", "missingsection2.config"))
def test_loadconfig_missingsections(filename):
    config_file_missingsection = os.path.join(_config_path, filename)

    with pytest.raises(botexceptions.MissingSection):
        _controller.load_config(config_file_missingsection)


def test_telegram_token():
    _controller.load_config(_config_file_valid)
    assert _controller._telegram_token == "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"


def test_spotify_username():
    _controller.load_config(_config_file_valid)
    assert _controller._spotify_username == "SpotifyUser"


class TestAccessConfig(object):
    _test_data = (
        (12354, True),
        (543431, True),
        (4711, False)
    )

    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._controller.load_config(_config_file_valid)

    @pytest.mark.parametrize("telegram_id, access_granted", _test_data)
    def test_has_access(self, telegram_id, access_granted):
        assert self._controller.has_access(telegram_id) == access_granted


@pytest.mark.parametrize("filename", ("missingusers1.config", "missingusers2.config"))
def test_loadconfig_missingusers(filename):
    config_file_missingusers = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingUsers):
        _controller.load_config(config_file_missingusers)


def test_duplicate_users():
    config_file_duplicate = os.path.join(_config_path, "duplicateusers.config")
    with pytest.raises(botexceptions.DuplicateUsers) as duplicate:
        _controller.load_config(config_file_duplicate)
    assert duplicate.value.duplicate_id == 12354


def test_loadconfig_badusers():
    config_file_badusers = os.path.join(_config_path, "badusers.config")
    with pytest.raises(botexceptions.InvalidUser) as invalid_exception:
        _controller.load_config(config_file_badusers)
    assert "bad_user" == invalid_exception.value.bad_id


@pytest.mark.parametrize("filename", ("missingtoken1.config", "missingtoken2.config"))
def test_loadconfig_missingtoken(filename):
    config_file_missingtoken = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingTelegramToken):
        _controller.load_config(config_file_missingtoken)


@pytest.mark.parametrize("filename", ("missingusername1.config", "missingusername2.config"))
def test_loadconfig_missingusername(filename):
    config_file_missingusername = os.path.join(_config_path, filename)
    with pytest.raises(botexceptions.MissingSpotifyUsername):
        _controller.load_config(config_file_missingusername)


class TestBookmarks(object):
    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._controller.load_config(_config_file_valid)

    @pytest.mark.parametrize("bookmark_name, spotify_id", (
            ("current", "5aftzefdrefg"),
            ("mybookmark", "zwdffee124455"),
            ("alpha", "34q1341441414"),
            ("bravo", "xadf45342424")))
    def test_loadconfig_bookmarks(self, bookmark_name, spotify_id):
        assert self._controller.get_bookmark(bookmark_name) == (spotify_id, None)


def test_loadconfig_duplicatebookmarks():
    config_file_duplicate = os.path.join(_config_path, "duplicatebookmarks.config")
    with pytest.raises(configparser.DuplicateOptionError):
        _controller.load_config(config_file_duplicate)
