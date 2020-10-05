from random import randint, shuffle
from collections import deque

from src.user import Player

from src.exceptions import (
    InsufficientFundsException,

    AlreadyInGameException,
    NoGameInProgressException,

    NoPlayersException,
    NotPlayersTurnException,
    PlayerNotFoundException,
)


class DreidelLogic:
    dreidel = {
        0: 'nun',
        1: 'gimel',
        2: 'hei',
        3: 'shin',
    }

    def __init__(self):
        self.pot = 0
        self.round = deque([])
        self.active_players = []

    def __str__(self):
        return f'Active Players: {self.round}, Pot: {self.pot}'

    @property
    def is_round_active(self):
        return len(self.round)

    def new_round(self) -> None:
        """
        Restarts the round.

        :return: None
        """
        shuffle(self.active_players)

        for player in self.active_players:
            self.round.append(player)

    def roll(self, user_obj: 'discord.User') -> str:
        """
        Rolls a dreidel and returns the result as a lowercased string.

        :param user_obj: discord.User
        :return: str
        """
        roll = DreidelLogic.dreidel[ randint(0, 3) ]

        if not self.is_round_active:
            raise NoGameInProgressException
        elif user_obj != self.ask_turn():
            raise NotPlayersTurnException

        user = self.round.pop()

        if roll == 'nun':
            pass
        elif roll == 'gimel':
            user.session_score = self.pot
            self.pot = 0
        elif roll == 'hei':
            # TODO: what if the pot is empty
            user.session_score = (self.pot // 2) + 1
            self.pot = (self.pot // 2) - 1
        elif roll == 'shin':
            try:
                self.put(user_obj, 1)
                user.session_score -= 1
            except InsufficientFundsException:
                raise

        return roll

    def put(self, user_obj: 'discord.User', pts: int) -> None:
        found_player = None

        if not self.active_players:
            raise NoPlayersException

        for i, player in enumerate(self.active_players):
            if user_obj == player.user_obj:
                found_player = player

        if found_player is None:
            raise PlayerNotFoundException
        elif found_player.bank < pts:
            raise InsufficientFundsException
        else:
            self.pot += pts
            found_player.bank -= pts

    def join(self, user_obj: 'discord.User') -> None:
        """
        Adds an user to the active players list and adds it last in the round doubly ended queue.

        :param user_obj: discord.User
        :return: None
        """

        active_players = (player.user_obj for player in self.active_players)

        if user_obj not in active_players:
            player = Player(user_obj)

            ( self.active_players ).append(player)

            # TODO: what if there's no round in progress?
            ( self.round ).appendleft(player)
        else:
            raise AlreadyInGameException

    def leave(self, user_obj: 'discord.User') -> None:
        active_players = (player.user_obj for player in self.active_players)

        if user_obj in active_players:
            # TODO: this looks horrible, refactor using the remove method
            for i, player in enumerate(self.active_players):
                if player.user_obj == user_obj:
                    del self.active_players[i]
                    break

            for i, player in enumerate(self.round):
                if player.user_obj == user_obj:
                    del self.round[i]
                    break
        else:
            raise PlayerNotFoundException

    def ask_turn(self) -> 'discord.User':
        """
        Peeks the last user in queue.

        :return: discord.User
        """
        try:
            player = ( self.round ).pop()
            ( self.round ).append(player)

            return player.user_obj
        except IndexError:
            raise NoPlayersException

