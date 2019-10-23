from rtmbot import RtmBot
import os

config = {
    'SLACK_TOKEN': os.environ.get('SLACK_TOKEN', None),
    'ACTIVE_PLUGINS': [
        'slackbot_plugins.conversation_average.ConversationAverage',
        'slackbot_plugins.total_average.TotalAverage'
    ]
}
if __name__ == '__main__':
    try:
        bot = RtmBot(config)
        bot.start()
    except Exception as e:
        print(e)
