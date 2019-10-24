import os
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
logger_file_path = '{0}{1}'.format(dir_path, '/slack_bot_logging.txt')

# Checking existence of log file directory. If not exists, create it
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
    open(logger_file_path, 'a').close()

# Checking existence of log file. If not exists, create it
if not os.path.exists(logger_file_path):
    open(logger_file_path, 'a').close()

def log(in_type, in_message):
    """
    Method that write messages into log file. Format of message "2019-10-21 21:13:56 [INFO] - Welcome to slackbot"
    :param in_type: INFO, WARNING, ERROR, etc.
    :param in_message: message for logging
    :return:
    """
    logger_file = open(logger_file_path, 'a')
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d  %H:%M:%S")
    log_string = '{0} [{1}] - {2}'.format(formatted_time, in_type, in_message)
    print(log_string, file=logger_file)
    logger_file.close()
