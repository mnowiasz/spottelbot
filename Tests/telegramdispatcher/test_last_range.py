import pytest

import botexceptions
import spotifycontroller
import telegramdispatcher


# Test the argument of /last
@pytest.mark.parametrize("value, expected, exception_expected", (
        (None, (1, spotifycontroller.last_limit), False),
        (["1"], (1, 1), False),
        ([str(spotifycontroller.last_limit + 5)], None, True),
        (["0"], None, True),
        (["foo"], None, True),
        (["1-5"], (1, 5), False),
        (["1-" + str(spotifycontroller.last_limit + 1), None, True]),
        (["-9"], (1, 9), False),
        (["1-", "5"], (1, 5), False),
        (["1", "-5"], (1, 5), False),
        (["1-", str(spotifycontroller.last_limit + 2)], None, True),
        (["1", "-", "7"], (1, 7), False),
        (["-5", "-", "3"], None, True),
        (["1", "-", "foobar"], None, True),
        (["1", "-", "2", "3", "4"], None, True)
))
def test_last_range(value, expected, exception_expected):
    if exception_expected:
        with  pytest.raises(botexceptions.InvalidRange):
            telegramdispatcher._last_range(value)
    else:
        assert expected == telegramdispatcher._last_range(value)
