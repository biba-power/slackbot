from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin, Job
from . import public_channel_id
from slackbot_engine.average_engine import AverageEngine

class getTotalAverage(Job):
    """Task that returns total average of all team members to the one public channel"""
    def run(self, slack_client):
        try:
            average_engine = AverageEngine(slack_client)
            all_channels_data = average_engine.get_data_for_all_channels()
            if all_channels_data['message_in_last_minute']:
                total_average = round(all_channels_data['total_sum']/all_channels_data['total_count'], 2)
                return_message = "Total average of all numbers in your direct message channels with me is: {0}".format(total_average)
                return [[public_channel_id, return_message]]
        except Exception as e:
            print(e)


class TotalAverage(Plugin):
    """A plugin that is responsible for calculating an average of numbers for the all direct message channels"""
    def register_jobs(self):
        job = getTotalAverage(60)
        self.jobs.append(job)
