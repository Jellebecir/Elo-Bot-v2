from mysql.connector import InterfaceError
from util.slack_util import SlackUtility

class Revert:
    def __init__(self, db_connector, request_data) -> None:
        self.requester_id = request_data['user_id']
        self.channel_id = request_data['channel_id']
        self.database = db_connector
        self.slack_util = SlackUtility()

    def execute(self):
        try:
            match = self.database.revert_latest_match(self.requester_id, self.channel_id)
            winner_name = self.slack_util.get_user_name_by_id(match[1])
            loser_name = self.slack_util.get_user_name_by_id(match[2])
            self.slack_util.client.chat_postMessage(
                channel=self.channel_id,
                text=f"The outcome of the most recent match between {winner_name} and {loser_name} has been reverted. This might have changed the leaderboard."
            )
        except InterfaceError:
            self.send_interface_error()
        except TypeError:
            self.slack_util.client.chat_postEphemeral(
                channel=self.channel_id,
                user=self.requester_id,
                text="Error: could not revert match because you have not played any matches."
            )

    def send_interface_error_message(self):
        self.slack_util.client.chat_postEphemeral(
            channel=self.channel_id,
            user=self.requester_id,
            text="Your revert request could not be completed due to an unresponsive server. Please try again later."
        )