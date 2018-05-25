"""Custom exception where the builin exceptions won't suffice"""


# Invalid user in the configfile (non-numeric UserID)
class InvalidUser(ValueError):
    def __init__(self, super_exception, userid):
        super(InvalidUser, self).__init__(super_exception)
        self.bad_id = userid


# No Token or empty token defined
class MissingTelegramToken(Exception):
    pass


# No users (or empty users). This is perfectly OK when starting the bot for the first time, hence a warning
# will suffice
class MissingUsers(Exception):
    pass


class DuplicateUsers(Exception):
    def __init__(self, telegram_id=None):
        self.duplicate_id = telegram_id


# No username (or empty username) for spotify
class MissingSpotifyUsername(Exception):
    pass

# A section is missing
class MissingSection(Exception):
    def __init__(self, section=None):
        self.missing_section = section
