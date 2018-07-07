import datetime

import dateutil.tz

from spottelbot import spotifycontroller, botconfig

# Played at today

_dummy_config = botconfig.BotConfig()
_controller = spotifycontroller.SpotifyController(_dummy_config)


def test_format_date_today():
    today = datetime.datetime.now(dateutil.tz.tzlocal())
    formatted = _controller._format_played_at(today.isoformat())

    assert formatted.startswith("Today")


def test_format_date_yesterdax():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    formatted = _controller._format_played_at(yesterday.isoformat())

    assert formatted.startswith("Yesterday")
