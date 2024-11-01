class BaseTeamsBotException(Exception):
    """Base Exception class for Teams bot"""


class ResourceNotFoundException(BaseTeamsBotException):
    """Raised when resource is not found"""


class UnknownAPIException(BaseTeamsBotException):
    """Raised when unknown API error occurs"""