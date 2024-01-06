
class Score:
    def __init__(self, db_connector, request_ids) -> None:
        requester_id = request_ids['loser']
        opponent_id = request_ids['winner']
        channel_id = request_ids['channel']
        self.score = db_connector.get_score_between_players(requester_id, opponent_id, channel_id)
    
    def execute(self):
        pass