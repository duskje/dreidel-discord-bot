class InsufficientFundsException(Exception):
    pass


class PlayerNotFoundException(Exception):
    pass


class UserNotInGameException(Exception):
    pass


class NoPlayersException(Exception):
    pass


class AlreadyInGameException(Exception):
    pass


class NotPlayersTurnException(Exception):
    pass

class NoGameInProgressException(Exception):
    pass