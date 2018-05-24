import os

import pytest

import botcontroller

_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.config")
_controller = botcontroller.BotController()


def test_loadconfig_nonexistent():
    with  pytest.raises(FileNotFoundError):
        _controller.load_config("broken.config")


def test_loadconfig():
    _controller.load_config(_config_file)


def test_telegram_token():
    _controller.load_config(_config_file)
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
        cls._controller.load_config(_config_file)

    @pytest.mark.parametrize("telegram_id, access_granted", _test_data)
    def test_has_access(self, telegram_id, access_granted):
        assert self._controller.has_access(telegram_id) == access_granted
