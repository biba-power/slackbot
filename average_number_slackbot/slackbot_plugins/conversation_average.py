from __future__ import print_function
from rtmbot.core import Plugin
from slackbot_engine.average_engine import AverageEngine
from slackbot_engine.utils import return_numbers
from slackbot_engine.exceptions import NoNumbersForwarded, NotPrivateChannel, NoMessagesInChannel


class ConversationAverage(Plugin):
    """A plugin that is responsible for calculating an average of numbers for the triggered channel"""

    def process_message(self, data):
        '''
        Method that is occurred when bot sees a message
        :param data: data that contains a message info
        :return: The average of numbers for the channel of the message if the channel is a private, and message contain
        a number
        '''
        try:
            message = data['text']
            current_channel = data['channel']
            self._check_channel_privacy(current_channel)
            average_engine = AverageEngine(self.slack_client)
            channel_data = average_engine.get_data_for_channel(current_channel)
            average = round(channel_data['numbers_sum'] / channel_data['numbers_count'], 2)

            # Check if numbers exists in last message. If not except NoNumbersForwarded
            return_numbers(message)
            self.outputs.append([current_channel, 'The average of numbers for this channel is: {0}'.format(average)])
        except NoMessagesInChannel:
            return

        except NotPrivateChannel:
            return

        except NoNumbersForwarded:
            self.outputs.append([current_channel,
                                 'Hmm.. There is no number/s in your previous message. The last average was: {0}'.format(
                                     average)])

        except Exception as e:
            print(e)
            return

    def _check_channel_privacy(self, channel_id):
        '''
        Method that check is channel private
        :param channel_id: id of a channel
        :return: Nothing if channel is private, otherwise raise NotPrivateChannel exception
        '''
        channel_data = self.slack_client.api_call('conversations.info', channel=channel_id)['channel']
        if 'is_private' in channel_data:
            if not channel_data['is_private']:
                raise NotPrivateChannel
