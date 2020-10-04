from random import randint, shuffle
from collections import deque

from exceptions import (
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
        shuffle(self.active_players)

        for player in self.active_players:
            self.round.append(player)

    def roll(self, user_obj) -> str:
        roll = DreidelLogic.dreidel[ randint(0, 3) ]

        if not len(self.round) or user_obj != self.ask_turn():
            raise NotPlayersTurnException

        try:
            user = self.round.pop()
        except IndexError:
            raise NoPlayersException

        if roll == 'nun':
            pass
        elif roll == 'gimel':
            user.session_score = self.pot
            self.pot = 0
        elif roll == 'hei':
            user.session_score = (self.pot // 2) + 1
            self.pot = (self.pot // 2) - 1
        elif roll == 'shin':
            user.session_score -= 1

            try:
                self.put(user_obj, 1)
            except InsufficientFundsException:
                raise

        return roll

    def put(self, user_obj, pts: int) -> None:
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
#
#    @staticmethod
#    def take(player: 'Player') -> None:
#        player.bank += player.session_score
#        player.session_score = 0

    def join(self, user_obj) -> None:
        active_players = (player.user_obj for player in self.active_players)

        if user_obj not in active_players:
            player = Player(user_obj)

            ( self.active_players ).append(player)
            ( self.round ).appendleft(player)
        else:
            raise AlreadyInGameException

    def leave(self, user_obj) -> None:
        active_players = (player.user_obj for player in self.active_players)

        if user_obj in active_players:
            # TODO: this looks horrible, refactor
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
        try:
            player = ( self.round ).pop()
            ( self.round ).append(player)

            return player.user_obj
        except IndexError:
            raise NoPlayersException


class Player:
    def __init__(self, user_obj):
        self.user_obj = user_obj
        self.session_score = 0
        self.bank = 100

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __repr__(self):
        return f'Player({self.user_id})'

    @property
    def user_id(self):
        return self.user_obj.id

    @classmethod
    def from_id(cls, user_id: int) -> 'Player':
        return cls(user_id)

    # TODO: Implement serialization
    def load_bank(self):
        pass

    def save(self):
        pass
