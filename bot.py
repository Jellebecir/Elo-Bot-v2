import os
from db_connector import DBConnector
from util.slack_util import SlackUtility
from util.exceptions import RequestWithUserTagException
from beatme import BeatMe
from leaderboard import Leaderboard
from score import Score

class EloBot:
    
    def __init__(self) -> None:
        self.bot_id = os.environ['BOT_ID']
        self.database = DBConnector()
        self.slack_util = SlackUtility()

    def handle_member_joined(self, payload):
        event = payload.get('event', {})
        channel_id = event.get('channel')
        user_id = event.get('user')

        if user_id == self.bot_id:
            self.database.create_channel_table(channel_id)
        elif self.database.user_in_channel_table(user_id, channel_id):
            self.send_welcome_back_message(user_id, channel_id)
        else:
            self.send_welcome_message(user_id, channel_id)

    def send_welcome_back_message(self, user_id, channel_id):
        state = self.database.get_channel_state(channel_id)
        user_data = state.get_player_data([user_id])[user_id]
        user_name = self.slack_util.get_user_name_by_id(user_id)

        message = f"Welcome back {user_name}!\n" \
                    f"Even though you left, we kept your records.\n" \
                    f" Your rating in this channel is {user_data['rating']}.\n"

        if user_data['ranking']:
            message += f" You are ranked #{user_data['ranking']} in this channel."
        else:
            message += "Unfortunately you have less than 5 matches played which means you do not qualify for a rank."
        
        self.slack_util.client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=message
        )

    def send_welcome_message(self, user_id, channel_id):
        message = "Hey there, welcome to this Slack channel!\n\n" \
                    "I'm Elo Bot. I keep track of the matches played in this channel. " \
                    "Any time you play a match against someone, " \
                    "your rating will be updated based on the outcome " \
                    "of the game and the rating of your opponent. " \
                    "Over time, you'll see how you're progressing and " \
                    "how you stack up against other players in the channel.\n\n" \
                    "To get started, challenge someone to a game and let me take care of the rest! " \
                    "You can find out how with the _/elo-bot-help_ command. " \
                    "Here you'll see a list of all bot commands and a more extensive " \
                    "explanation of the Elo system.\n\n" \
                    "If you have any other questions or feedback, feel free to send Jelle a message."
        self.slack_util.client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=message
        )

    def handle_beatme(self, request_data):
        try:
            request_ids = self.slack_util.get_ids_from_tagged_request(request_data)
            BeatMe(self.database, request_ids).execute()
        except RequestWithUserTagException as err:
            self.slack_util.client.chat_postEphemeral(
                channel=request_data['channel_id'],
                user=request_data['user_id'],
                text=err.message
            )

    def handle_leaderboard(self, request_data):
        channel_id = request_data.get('channel_id')
        state = self.database.get_channel_state(channel_id)
        Leaderboard(state, channel_id).execute()

    def handle_score(self, request_data):
        try:
            request_ids = self.slack_util.get_ids_from_tagged_request(request_data)
            Score(self.database, request_ids).execute()
        except RequestWithUserTagException as err:
            self.slack_util.client.chat_postEphemeral(
                channel=request_data['channel_id'],
                user=request_data['user_id'],
                text=err.message
            )
