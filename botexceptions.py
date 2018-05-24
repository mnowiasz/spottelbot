"""Custom exception where the builin exceptions won't suffice"""


# Invalid user in the configfile (non-numeric UserID)
class InvalidUser(ValueError):
    def __init__(self, super_exception, userid):
        super(InvalidUser, self).__init__(super_exception)
        self.bad_id = userid


# No Token or empty token defined
class MissingTelegramToken(Exception):
    pass


# A section is missing
class MissingSection(Exception):
    pass
