from util.calculate_elo import calculate_new_ratings
from player import Player

class State:
    def __init__(self, matches) -> None:
        self.state = {}
        for match in matches:
            winner_id = match[0]
            loser_id = match[1]
            if winner_id not in self.state:
                self.state[winner_id] = Player(winner_id)
            if loser_id not in self.state:
                self.state[loser_id] = Player(loser_id)

            self.mock_record_match(winner_id, loser_id)
    
    def get_player(self, player_id):
        return self.state[player_id]
    
    def get_snapshot(self):
        # Sort players in state based on rating
        sorted_players = sorted(self.state.items(), key=lambda item: item[1].rating, reverse=True)
        ranked_players = {}
        # Take into account players that are not qualified to be ranked
        n_players_not_qualified = 0
        for index in range(0, len(sorted_players)):
            player = sorted_players[index][1]

            # If player is qualified, assign them their rank, corrected for amount of players that are not qualified
            if player.is_qualified():
                rank = index - n_players_not_qualified + 1
                player.set_ranking(rank)
                # Make copy of player so that future references to player from this state are correct
                ranked_players[player.id] = player.copy()

            else:
                n_players_not_qualified += 1

        return ranked_players

    def get_qualified_state(self):
        """
        Returns the state when only taking players that have played more than 5 games
        """
        return {k: player for k, player in self.state.items() if player.is_qualified()}

    def get_player_data(self, ids):
        """
        Returns rating and ranking for a given user ID
        """
        # Calculate rating
        qualified_state = self.get_qualified_state()
        data = {}
        
        for player_id in ids:
            try:
                player = qualified_state[player_id]
                ranking = self.get_user_ranking(qualified_state, player)
                player.set_ranking(ranking)
            except KeyError:
                player = self.state[player_id]
            # Calculate ranking
            data[player_id] = player
        
        return data
    
    def get_player_unranked_data(self, player_id):
        print(self.state)
        player = self.state[player_id]
        return {
            'rating': player.change,
            'rank': None
        }

    def get_user_ranking(self, state, player):
        sorted_ratings = sorted(state.items(), key=lambda x: x[1].rating, reverse=True)
        return next((index for index, item in enumerate(sorted_ratings) if item[0] == player.id), None) + 1
    
    def mock_record_match(self, winner_id, loser_id):
        """
        Records match in local state. Does NOT add event to the event source (database).
        """
        if not winner_id in self.state.keys():
            self.state[winner_id] = Player(winner_id)
        if not loser_id in self.state.keys():
            self.state[loser_id] = Player(loser_id)

        new_ratings = calculate_new_ratings(self.state[winner_id].rating, self.state[loser_id].rating)
        self.state[winner_id].update_player_stats(new_ratings['winner'], True)
        self.state[loser_id].update_player_stats(new_ratings['loser'], False)

    def get_snapshot_diffs(self, old_ranked_state):
        current_ranked_state = self.get_snapshot()
        qualified_players = current_ranked_state.keys()
        state_diffs = {}
        for player_id in qualified_players:

            if not player_id in old_ranked_state.keys():
                state_diffs[player_id] = {'rating': abs(1200 - current_ranked_state[player_id].rating), 'rank': 0}

            else:
                # Calculate difference in player stats before and after match
                old_player_state = old_ranked_state[player_id]
                new_player_state = current_ranked_state[player_id]
                player_changes = old_player_state.get_player_changes(new_player_state)

                # If change has occured, add to state changes
                if player_changes['rating'] or player_changes['rank']:
                    state_diffs[player_id] = player_changes

        return state_diffs