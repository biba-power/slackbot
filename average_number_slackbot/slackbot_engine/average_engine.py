from slackclient import SlackClient
from datetime import datetime
from .utils import return_numbers
from .exceptions import NoNumbersForwarded, MemberDoesNotExist, MemberDoesNotHaveDmc, NoMessagesInChannel
import os


class AverageEngine:
    """
    Engine that will be responsible for calculating average of numbers of all direct message channels or single
    direct message channel
    """

    def __init__(self, slack_client=None):
        if slack_client is None:
            self._create_slack_client()
        else:
            self.slack_client = slack_client

    def get_data_for_channel(self, channel_id):
        """
        A method that returns a dictionary that contains next data for the direct message channel:
            - numbers_sum: sum of the numbers in channel
            - numbers_count: count of the numbers in channel
            - last_message_date: datetime of last message
        :param channel_id: id of a channel
        :return: dictionary if everything is ok, otherwise can raise next exceptions:
            - NoMessagesInChannel: if channel does not have messages
        """
        conversation_data = self.slack_client.api_call("conversations.history", channel=channel_id)
        messages_list = conversation_data['messages']
        if 'response_metadata' in conversation_data:
            if 'next_cursor' in conversation_data['response_metadata']:
                next_cursor_data = self.slack_client.api_call("conversations.history", channel=channel_id,
                                                          cursor=conversation_data['response_metadata']['next_cursor'])
                messages_list.extend(next_cursor_data['messages'])
        if len(messages_list) < 1:
            raise NoMessagesInChannel('There is no messages in this channel')
        numbers_count = 0
        numbers_sum = 0
        greatest_time = datetime.fromtimestamp(float(messages_list[0]['ts']))
        for message in messages_list:
            if 'bot_id' not in message:
                try:
                    message_numbers = return_numbers(message['text'])
                    numbers_sum += sum(message_numbers)
                    numbers_count += len(message_numbers)
                except NoNumbersForwarded:
                    pass
                except ValueError:
                    pass
                message_date = datetime.fromtimestamp(float(message['ts']))
                if message_date > greatest_time:
                    greatest_time = message_date

        return_dict = {
            'numbers_sum': numbers_sum,
            'numbers_count': numbers_count,
            'last_message_date': greatest_time
        }
        return return_dict

    def get_data_for_all_channels(self):
        """
        A method that returns a dictionary that contains next data for all direct message channels:
            - numbers_sum: sum of the numbers in all direct message channels
            - numbers_count: count of the numbers in all direct message channels
            - message_in_last_minute: True if a new message exists in the last minute, otherwise False
        :return: dictionary with data for all direct message channels
        """
        channels = self._get_all_dmc()
        total_sum = 0
        total_count = 0
        now = datetime.now()
        message_in_last_minute = False
        for channel in channels:
            try:
                channel_data = self.get_data_for_channel(channel['id'])
            except NoMessagesInChannel:
                pass
            if channel_data is not None:
                total_sum += channel_data['numbers_sum']
                total_count += channel_data['numbers_count']
                time_diff = (now - channel_data['last_message_date']).total_seconds() / 60.0
                if time_diff < 1:
                    message_in_last_minute = True

        return_dict = {
            'total_sum': total_sum,
            'total_count': total_count,
            'message_in_last_minute': message_in_last_minute
        }
        return return_dict

    def get_channel_id(self, in_member_name):
        """
        Method that returns id of direct message channel between member and Bot
        :param in_member_name: slack name of the member
        :return: id of channel if exists, otherwise raise MemberDoesNotHaveDmc exception
        """
        member_id = self._get_member_id(in_member_name)
        all_dmc_channels = self._get_all_dmc()
        for dmc_channel in all_dmc_channels:
            if member_id == dmc_channel['user']:
                return dmc_channel['id']
        else:
            raise MemberDoesNotHaveDmc

    # Private methods
    def _get_member_id(self, in_member_name):
        """
        Method that returns id of a member that has name equal to input parameter in_member_name
        :param in_member_name:  name of a slack member
        :return: id of a member, otherwise raise MemberDoesNotExist exception
        """
        try:
            team_members = self.slack_client.api_call('users.list')['members']
            for member in team_members:
                if member['name'] == in_member_name:
                    return member['id']
            else:
                raise MemberDoesNotExist
        except MemberDoesNotExist:
            raise MemberDoesNotExist('Member with username {0} does not exist!'.format(in_member_name))

    def _get_all_dmc(self):
        """
        Method that returns all direct message channels of the bot user
        :return: list of direct message channels
        """
        return self.slack_client.api_call('im.list')['ims']

    def _create_slack_client(self):
        """
        Method that creates SlackClient object
        :return:
        """
        try:
            SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
            slack_client = SlackClient(SLACK_TOKEN)
            slack_client.rtm_connect()
            self.slack_client = slack_client
        except Exception as e:
            raise Exception(e)
