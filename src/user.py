class Player:
    def __init__(self, user_obj: 'discord.User'):
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
