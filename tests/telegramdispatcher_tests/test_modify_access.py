""" Test /adduser and /deluser commands"""

import pytest

import botconfig
import botexceptions
import telegramdispatcher
from tests.testdata import TestAccessData


class TestRemoveAccess(TestAccessData):

    @pytest.mark.parametrize("telegram_ids, exception_expected", (
            (["1"], False),
            (["nosuchuser"], True),
            (["3", "4", "@myaccount"], False)
    ))
    def test_remove_access(self, telegram_ids, exception_expected):
        test_dispatcher = telegramdispatcher.TelegramDispatcher(self._test_config, None)

        if exception_expected:
            with pytest.raises(KeyError):
                test_dispatcher.deluser(telegram_ids)
        else:
            test_dispatcher.deluser(telegram_ids)
            for single_id in telegram_ids:
                assert not self._test_config.has_access(single_id)


class TestAddAccess(object):

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.BotConfig()
        cls._test_dispatcher = telegramdispatcher.TelegramDispatcher(cls._test_config, None)

    @pytest.mark.parametrize("telegram_ids, exception_expected", (
            (["1"], False),
            (["nosuchuser"], True),
            (["2", "3", "@"], True),
            (["@myaccount", "522442"], False)
    ))
    def test_add_access(self, telegram_ids, exception_expected):
        if exception_expected:
            with pytest.raises((KeyError, botexceptions.InvalidUser)):
                self._test_dispatcher.adduser(telegram_ids)
        else:
            self._test_dispatcher.adduser(telegram_ids)
            for single_id in telegram_ids:
                assert self._test_config.has_access(single_id)
