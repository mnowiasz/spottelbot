""" The Main file"""
import configparser
import logging
import sys
from pathlib import Path

from spottelbot import botconfig
from spottelbot import botexceptions
from spottelbot import spotifycontroller
from spottelbot import telegramcontroller

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

_config_locations = ("spottelbot.config", "spottelbot/config", ".spottelbot/config")


def botmain():
    # Which configfile to use? If a parameter is given, this should be the configfile. If not, look for it at
    # several locations

    if len(sys.argv) > 2:
        print("Usage: %s <configfile>" % sys.argv[0])
        exit(1)

    if len(sys.argv) == 2:
        configfile = Path(sys.argv[1])
    else:
        # Current directory and $HOME
        for path in (Path.cwd(), Path.home()):
            for location in _config_locations:
                configfile = (Path(path) / location).resolve()
                if configfile.is_file():
                    break
            else:
                # Looped through all alternatives -> no configfile found
                configfile = None
            # Break from the inner loop? Break the outer loop if found
            if configfile:
                break
        else:
            # Finished, no luck
            configfile = None

    if not configfile:
        print("Unable to find configfile!")
        exit(1)
    try:
        config = botconfig.BotConfig()
        config.load_config(configfile)
        spotify_controller = spotifycontroller.SpotifyController(config)
        spotify_controller.connect()
        telegram_controller = telegramcontroller.TelegramController(config, spotify_controller)
        telegram_controller.connect()
    except botexceptions.InvalidUser as invalid:
        print("Invalid User " + invalid.bad_id)
        exit(1)
    except botexceptions.InvalidBookmark as invalid:
        print("Invalid bookmark " + invalid.invalid_bookmark)
        exit(1)
    except botexceptions.DuplicateUsers as duplicate:
        print("Duplicate User " + duplicate.duplicate_id)
        exit(1)
    except botexceptions.MissingUsers:
        print("No user defined!")
        exit(1)
    except botexceptions.MissingSection as missing:
        print("Missing config section " + missing.missing_section)
        exit(1)
    except botexceptions.MissingTelegramToken:
        print("Missing telegram token")
        exit(1)
    except botexceptions.MissingSpotifyUsername:
        print("Missing spotify username")
    except configparser.MissingSectionHeaderError:
        print("No sections in configfile")


if __name__ == '__main__':
    botmain()
