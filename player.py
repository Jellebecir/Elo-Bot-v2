
class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.wins = 0
        self.losses = 0
        self.change = 0
        self.rating = 1200
        self.rank = 'unqualified'

    def update_player_stats(self, new_rating, won_match):
        # if user won, rating change should be positive, else should be negative
        outcome_modifier = 1 if won_match else -1

        # update change in rating, rating and number of losses/wins
        self.change = round(abs(self.rating - new_rating)) * outcome_modifier
        self.rating = new_rating
        self.add_win() if won_match else self.add_loss()

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def is_qualified(self):
        return self.wins + self.losses > 5
    
    def set_ranking(self, rank):
        self.rank = rank

    def get_player_changes(self, new_player_state):
        rating_change =  abs(self.rating - new_player_state.rating)
        if self.rank is not 'unqualified':
            rank_change = self.rank - new_player_state.rank
        else:
            rank_change = 0
        return {'rating': rating_change, 'rank': rank_change}
    
    def copy(self):
        copy = Player(self.id)
        copy.wins = self.wins
        copy.losses = self.losses
        copy.change = self.change
        copy.rating = self.rating
        copy.set_ranking(self.rank)
        return copy

    def __str__(self) -> str:
        return str({
            'id': self.id,
            'rating': self.rating,
            'wins': self.wins,
            'losses': self.losses,
            'change': self.change,
            'rank': self.rank
            })