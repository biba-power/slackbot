from slackclient import SlackClient
from datetime import datetime
from .utils import return_numbers
from .exceptions import NoNumbersForwarded, MemberDoesNotExist, MemberDoesNotHaveDmc, NoMessagesInChannel
from .logger_handler import log
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
        log('INFO', 'Get data for channel')
        conversation_data = self.slack_client.api_call("conversations.history", channel=channel_id)
        messages_list = self._get_messages_from_channel(conversation_data, channel_id, [])
        if len(messages_list) < 1:
            log('ERROR', 'This channel has no messages')
            raise NoMessagesInChannel('There is no messages in this channel')
        numbers_count = 0
        numbers_sum = 0
        greatest_time = datetime.fromtimestamp(float(messages_list[0]['ts']))
        log('INFO', 'This channel has {0} messages'.format(len(messages_list)))
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
        log('INFO', 'Data of this channel is {0}'.format(return_dict))
        return return_dict

    def get_data_for_all_channels(self):
        """
        A method that returns a dictionary that contains next data for all direct message channels:
            - numbers_sum: sum of the numbers in all direct message channels
            - numbers_count: count of the numbers in all direct message channels
            - message_in_last_minute: True if a new message exists in the last minute, otherwise False
        :return: dictionary with data for all direct message channels
        """
        log('INFO', 'Get data for all messages')
        channels = self._get_all_dmc()
        log('INFO', 'Number of channels'.format(len(channels)))
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
        log('INFO', 'Data of all channels is {0}'.format(return_dict))
        return return_dict

    def get_channel_id(self, in_member_name):
        """
        Method that returns id of direct message channel between member and Bot
        :param in_member_name: slack name of the member
        :return: id of channel if exists, otherwise raise MemberDoesNotHaveDmc exception
        """
        log('INFO', 'Get channel id for {0} member'.format(in_member_name))
        member_id = self._get_member_id(in_member_name)
        all_dmc_channels = self._get_all_dmc()
        for dmc_channel in all_dmc_channels:
            if member_id == dmc_channel['user']:
                return dmc_channel['id']
        else:
            log('ERROR', 'Member does not have direct message channel')
            raise MemberDoesNotHaveDmc

    # Private methods
    def _get_messages_from_channel(self, in_conversation_data, in_channel_id, messages_list):
        """
        Method that returns all messages on the channel. Slack API limits the number of return messages in a single
        call to 100 and give the next_cursor string in response_metadata which means that there are more messages for
        this channel. This method will be called recursively until there is a cursor in the response_metadata
        :param in_conversation_data: data of the conversation which contain messages
        :param in_channel_id: id of a channel
        :param messages_list: list of messages
        :return:list of all messages
        """
        try:
            messages_list.extend(in_conversation_data['messages'])
            if 'response_metadata' in in_conversation_data:
                if 'next_cursor' in in_conversation_data['response_metadata']:
                    log('INFO', 'Channel has more than {0} messages'.format(len(messages_list)))
                    next_cursor_data = self.slack_client.api_call("conversations.history", channel=in_channel_id,
                                                              cursor=in_conversation_data['response_metadata']['next_cursor'])
                    self._get_messages_from_channel(next_cursor_data, in_channel_id, messages_list)

            return messages_list
        except Exception as e:
            log('ERROR', 'Error in _get_messages_from_channel. Stack trace {0}'.format(str(e)))

    def _get_member_id(self, in_member_name):
        """
        Method that returns id of a member that has name equal to input parameter in_member_name
        :param in_member_name:  name of a slack member
        :return: id of a member, otherwise raise MemberDoesNotExist exception
        """
        try:
            log('INFO', 'Get id of {0} member'.format(in_member_name))
            team_members = self.slack_client.api_call('users.list')['members']
            for member in team_members:
                if member['name'] == in_member_name:
                    return member['id']
            else:
                log('ERROR', 'Member does not exist')
                raise MemberDoesNotExist
        except MemberDoesNotExist:
            raise MemberDoesNotExist('Member with username {0} does not exist!'.format(in_member_name))

    def _get_all_dmc(self):
        """
        Method that returns all direct message channels of the bot user
        :return: list of direct message channels
        """
        log('INFO', 'Get all direct message channels')
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
            log('ERROR', 'Something went wrong in _create_slack_client. Stack trace: {0}'.format(str(e)))
            raise Exception(e)
