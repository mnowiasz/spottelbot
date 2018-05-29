""" Tests of the mark / bookmark features"""
import random
import string

import botcontroller
import telegramdispatcher


# /mark without any parameter
def test_mark_current(monkeypatch):
    track_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))

    def mockget_current():
        return (track_id, None)

    controller = botcontroller.BotController()

    dispatcher = telegramdispatcher.TelegramDispatcher(controller)

    monkeypatch.setattr(controller.spotify_controller, "get_current", mockget_current, raising=False)

    dispatcher.mark(None)

    assert (track_id, None) == controller.get_bookmark(botcontroller.bookmark_current)
