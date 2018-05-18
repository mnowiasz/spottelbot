""" The users allowed to communicate with the bot"""
import telegram

# Since initially we don't know telegram's UUID of the given username, this function is needed to obtain it

def whoami() -> telegram.User:
    return telegram.User(1, "Bot", False)



