import pytest

import botcontroller


def test_botname():
    test_config = botcontroller.BotController()
    assert "MyBot" == test_config.botname


class TestAcess(object):
    _test_data = (
        # ID, Access granted, exception raised (add)
        (1, True, False),
        (2, False, False),
        (3, True, False),
        (4, True, False),
        (4, True, True),
        (1, True, True)
    )

    @classmethod
    def setup_class(cls):
        cls._test_controller = botcontroller.BotController()
        for item in cls._test_data:
            telegram_id, access_granted, exception_expected = item
            if access_granted:
                if exception_expected:
                    with pytest.raises(KeyError):
                        cls._test_controller.add_access(telegram_id)
                else:
                    cls._test_controller.add_access(telegram_id)

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_has_access(self, telegram_id, access_granted, exception_expected):
        if exception_expected:
            pass
        assert access_granted == self._test_controller.has_access(telegram_id)

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", _test_data)
    def test_remove_access(self, telegram_id, access_granted, exception_expected):
        # If an exception was expected the duplicate ID wasn't added. However, the original ID was added
        if exception_expected:
            pass
        elif not access_granted:
            with  pytest.raises(KeyError):
                self._test_controller.remove_access(telegram_id)
        else:
            self._test_controller.remove_access(telegram_id)
            assert not self._test_controller.has_access(telegram_id)
