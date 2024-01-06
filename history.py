from texttable import Texttable
from util.slack_util import SlackUtility

class Histroy:
    def __init__(self, db_connector, request_data) -> None:
        self.database = db_connector
        self.channel_id = request_data.get('channel_id')
        self.requester_id = request_data['user_id']
        self.slack_util = SlackUtility()

    def execute(self):
        history = self.database.get_history(self.requester_id, self.channel_id)
        if len(history) == 0:
            self.slack_util.client.chat_postEphemeral(
                channel=self.channel_id,
                user=self.requester_id,
                text="Can not provide a history because you have played not matches in this channel."
            )
        else:
            table = self.get_history_table(history)
            self.slack_util.client.chat_postEphemeral(
                channel=self.channel_id,
                user=self.requester_id,
                text=table
            )

    def get_history_table(self, history):
        table = Texttable()
        table.header(["Opponent", "Winner", "Date"])
        for match in history:
            winner_id = match[1]
            loser_id = match[2]
            date = match[3]
            
            if winner_id == self.requester_id:
                opponent_name = self.slack_util.get_user_name_by_id(loser_id)
                table.add_row([opponent_name, "You", date])
            else:
                opponent_name = self.slack_util.get_user_name_by_id(winner_id)
                table.add_row([opponent_name, opponent_name, date])
        table.set_deco(Texttable.HEADER)
        return "```" + table.draw().replace('=', '') + "```"