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


def test_telegram_token():
    _controller.load_config(_config_file_valid)
    assert _controller._telegram_token == "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"


class TestAccessConfig():
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


def test_loadconfig_missingusers():
    config_file_nousers = os.path.join(_config_path, "missingusers.config")
    with pytest.raises(KeyError) as keyerror:
        _controller.load_config(config_file_nousers)
    assert _controller._telegram_entry_users == keyerror.value.args[0]


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


# TODO: Missingsection2
@pytest.mark.parametrize("filename", ("missingsection1.config", "missingsection1.config"))
def test_loadconfig_missingsections(filename):
    config_file_missingsection = os.path.join(_config_path, filename)

    with pytest.raises(botexceptions.MissingSection):
        _controller.load_config(config_file_missingsection)
