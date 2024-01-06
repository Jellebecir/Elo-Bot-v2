from texttable import Texttable
from util.slack_util import SlackUtility

class Score:
    def __init__(self, db_connector, request_ids) -> None:
        self.slack_util = SlackUtility()
        self.requester_id = request_ids['requester']
        self.opponent_id = request_ids['opponent']
        self.opponent_name = self.slack_util.get_user_name_by_id(self.opponent_id)
        self.channel_id = request_ids['channel']
        
        self.score = db_connector.get_score_between_players(
            self.requester_id, 
            self.opponent_id, 
            self.channel_id
            )
    
    def execute(self):
        self.slack_util.client.chat_postEphemeral(
            channel=self.channel_id,
            user=self.requester_id,
            text=self.get_score_message()
        )

    def get_score_message(self):
        rows = []
        for player_id in list(self.score.keys()):
            row = []

            if player_id == self.requester_id:
                row.append("You")
            else:
                row.append(self.opponent_name)

            row.append(self.score[player_id])
            row.append(self.get_winner_indicator(player_id))
            rows.append(row)
        
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.add_rows(rows, False)
        return f"Your score against {self.opponent_name}\n```" + table.draw() + "```"


    def get_winner_indicator(self, player_id):
        if self.player_has_highest_score(player_id):
            return '👑'
        else:
            return ''
        
    def player_has_highest_score(self, player_id):
        value = self.score[player_id]
        highest_value = max(self.score.values())

        if value == highest_value and list(self.score.values()).count(value) == 1:
            return True
        else:
            return False

    def player_has_highest_score(self, player_id):
        value = self.score[player_id]
        highest_value = max(self.score.values())

        if value == highest_value and list(self.score.values()).count(value) == 1:
            return True
        else:
            return False
    