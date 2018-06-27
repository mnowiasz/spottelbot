""" The Main file"""
import logging

import botconfig
import spotifycontroller
import telegramdispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def botmain():
    config = botconfig.BotConfig()
    config.load_config(open("/home/nowiasz/.spottelbot/config"))
    spotify_controller = spotifycontroller.SpotifyController()
    dispatcher = telegramdispatcher.TelegramDispatcher(config, spotifycontroller)
    dispatcher.connect()

    # TODO: Exceptions, commandline options


if __name__ == '__main__':
    botmain()
