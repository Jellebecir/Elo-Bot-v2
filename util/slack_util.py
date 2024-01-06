import os
import re
import slack
from util.exceptions import *

class SlackUtility:
    def __init__(self) -> None:
        self.client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

    def validate_user_tagged_request(self, request_ids):
        if request_ids['winner'] == request_ids['loser']:
            raise SelfTagException()
        
        if request_ids['winner'] == os.environ['BOT_ID']:
            raise BotTagException()

        if not self.is_user_in_channel(request_ids['winner'], request_ids['channel']):
            raise UserNotInChannelException()


    def get_ids_from_tagged_request(self, request):
        """
        Returns the channel, tagged user id and requester id of a request that contains a tagged user.
        """
        channel_id = request.get('channel_id')
        loser_id = request.get('user_id')
        winner_name = self.parse_request_name(request.get('text'))
        winner_id = self.get_user_by_name(winner_name, channel_id)['id']
        request_ids = {'winner': winner_id, 'loser': loser_id, 'channel': channel_id}
        self.validate_user_tagged_request(request_ids)
        return request_ids

    def get_user_by_name(self, user_name, channel_id):
        channel_users = self.get_channel_users(channel_id=channel_id)
        for user in channel_users:
            if user['name'] == user_name:
                return user

    def is_user_in_channel(self, user_id, channel_id):
        client_response = self.client.conversations_members(channel=channel_id)
        if client_response['ok']:
            for member_id in client_response['members']:
                if member_id == user_id:
                    return True


    def get_channel_users(self, channel_id):
        """
        Gets all user IDs in the channel
        :param channel_id: string representing the channel ID
        :return: array of user IDs (string)
        """
        client_response = self.client.conversations_members(channel=channel_id)
        if client_response['ok']:
            all_users = []
            for member_id in client_response['members']:
                user = self.get_user_by_id(member_id)
                all_users.append(user)
            return all_users


    def get_user_by_id(self, user_id):
        user_response = self.client.users_info(user=user_id)
        if user_response['ok']:
            return user_response['user']


    def get_user_name_by_id(self, user_id):
        user_info = self.get_user_by_id(user_id)
        return self.get_user_name(user_info)


    def get_user_name(self, user):
        user_display_name = user['profile']['display_name']
        if not user_display_name:
            return user['profile']['real_name']
        else:
            return user_display_name


    def parse_request_name(self, name):
        pattern = r'@(.+)'
        match = re.match(pattern, name.split(" ")[0])
        if match:
            return match.group(1)
        else:
            raise InvalidUserTagException(name)
