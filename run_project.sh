cd average_number_slackbot;
filename=$PWD/slackbot_engine/slack_bot_logging.txt
if [ ! -f $filename ]
then
  touch $filename
fi
../venv/bin/python3 run_api.py &
../venv/bin/python3 run_bot.py &
