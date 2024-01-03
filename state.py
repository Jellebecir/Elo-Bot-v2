from util.calculate_elo import calculate_new_ratings

class State:
    def __init__(self, matches) -> None:
        self.state = {}
        for match in matches:
            winner_id = match[0]
            loser_id = match[1]
            if winner_id not in self.state:
                self.state[winner_id] = {'rating': 1200, 'wins': 0, 'losses': 0}
            if loser_id not in self.state:
                self.state[loser_id] = {'rating': 1200, 'wins': 0, 'losses': 0}

            self.record_match(winner_id, loser_id)
    
    def get_qualified_state(self):
        """
        Returns the state when only taking players that have played more than 5 games
        """
        return {k: v for k, v in self.state.items() if v['wins'] and v['losses'] > 5}

    def get_user_data(self, ids):
        """
        Returns rating and ranking for a given user ID
        """
        # Calculate rating
        qualified_state = self.get_qualified_state()
        sorted_ratings = sorted(qualified_state.items(), key=lambda x: x[1]['rating'], reverse=True)
        data = {}
        
        for user_id in ids:
            rating = qualified_state[user_id]['rating']
            # Calculate ranking
            if self.user_is_qualified(user_id):
                ranking = next((index for index, item in enumerate(sorted_ratings) if item[0] == user_id), None) + 1
            else:
                ranking = None
            data[user_id] = {'rating': rating, 'ranking': ranking}
        
        return data
    
    def user_is_qualified(self, user_id):
        """
        Returns if user has played more than 5 matches i.e. is qualified on the leaderboard.
        """
        qualified_state = self.get_qualified_state()
        return qualified_state[user_id]['wins'] + qualified_state[user_id]['losses'] > 5
    
    def record_match(self, winner_id, loser_id):
        """
        Records match in local state. Does NOT add event to the event source (database).
        """
        new_ratings = calculate_new_ratings(self.state[winner_id]['rating'], self.state[loser_id]['rating'])
        
        # update winner data
        self.state[winner_id]['rating'] = new_ratings['winner']
        self.state[winner_id]['wins'] += 1
        
        #update loser data
        self.state[loser_id]['rating'] = new_ratings['loser']
        self.state[loser_id]['losses'] += 1