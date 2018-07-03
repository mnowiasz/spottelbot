"""Custom exception where the builin exceptions won't suffice"""


# Invalid user in the configfile (non-numeric UserID with no "@")
class InvalidUser(Exception):
    def __init__(self, userid):
        self.bad_id = userid


# No Token or empty token defined
class MissingTelegramToken(Exception):
    pass


# No users (or empty users).
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


# Invalid Bookmarks (more than one or two entries)
class InvalidBookmark(Exception):
    def __init__(self, bookmark=None):
        self.invalid_bookmark = bookmark


# Invalid range/argument to /last or /mark
class InvalidRange(Exception):
    def __init__(self, argument=None):
        self.invalid_argument = argument


# Unable to connect to spotify
class SpotifyAuth(Exception):
    pass


# Max message length
class TelegramMessageLength(Exception):
    def __init__(self, length=0):
        self.invalid_length = length
