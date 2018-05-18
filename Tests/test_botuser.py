import botuser
import telegram

def test_whoami():
    my_id:telegram.User = botuser.whoami()
    assert my_id.id == 1
    assert my_id.is_bot == False
    assert my_id.first_name == "Bot"
