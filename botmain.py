""" The Main file"""
import logging

import botcontroller

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def botmain():
    controller = botcontroller.BotController()
    controller.config.load_config(open("/home/nowiasz/.spottelbot/config"))
    controller.telegram_dispatcher.connect()

    # TODO: Exceptions, commandline options


if __name__ == '__main__':
    botmain()
