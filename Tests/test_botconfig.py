import botconfig
import pytest


def test_botname():
    test_config = botconfig.Config()
    assert test_config.botname == "MyBot"


class TestAcess(object):
    _test_data = [
        # ID, Access granted, exception raised (add)
        (1, True, False),
        (2, False, False),
        (3, True, False),
        (4, True, False),
        (4, True, True),
        (1, True, True)
    ]

    @classmethod
    def setup_class(cls):
        cls._test_config = botconfig.Config()
        for item in cls._test_data:
            telegram_id, access_granted, exception_expected = item
            if access_granted:
                if exception_expected:
                    with pytest.raises(KeyError):
                        cls._test_config.add_access(telegram_id)
                else:
                    cls._test_config.add_access(telegram_id)

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_has_access(self, telegram_id, access_granted, exception_expected):
        if exception_expected:
            pass
        assert self._test_config.has_access(telegram_id) == access_granted

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_remove_access(self, telegram_id, access_granted, exception_expected):
        # If an exception was expected the ID wasn't added
        if exception_expected:
            pass
        elif not access_granted:
            with  pytest.raises(KeyError):
                self._test_config.remove_access(telegram_id)
        else:
            self._test_config.remove_access(telegram_id)
            assert not self._test_config.has_access(telegram_id)
