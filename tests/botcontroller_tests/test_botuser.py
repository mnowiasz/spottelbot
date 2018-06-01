import telegram

import botuser


def test_whoami():
    my_id:telegram.User = botuser.whoami()
    assert (1, False, "Bot") == (my_id.id, my_id.is_bot, my_id.first_name)
