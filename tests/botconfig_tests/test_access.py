import pytest

from spottelbot import botexceptions
from tests.testdata import TestAccessData


class TestAcess(TestAccessData):

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", TestAccessData._test_data)
    def test_has_access(self, telegram_id, access_granted, exception_expected):
        if exception_expected:
            pass
        assert access_granted == self._test_config.has_access(telegram_id)

    @pytest.mark.parametrize("telegram_id, access_granted, exception_expected", TestAccessData._test_data)
    def test_remove_access(self, telegram_id, access_granted, exception_expected):
        # If an exception was expected the duplicate ID wasn't added. However, the original ID was added
        if exception_expected:
            pass
        elif not access_granted:
            with  pytest.raises(KeyError):
                self._test_config.remove_access(telegram_id)
        else:
            self._test_config.remove_access(telegram_id)
            assert not self._test_config.has_access(telegram_id)

    @pytest.mark.parametrize("telegram_id", (
            "usernamewithout@", "@", "user@name"
    ))
    def test_illegal_username(self, telegram_id):
        with pytest.raises(botexceptions.InvalidUser):
            self._test_config.add_access(telegram_id)
