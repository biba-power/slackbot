# slackbot
Slackbot that calculates the average number of direct message channels.

This slack bot is created to respond on messages from other users of the workspace. 
The respose message of the bot will contain the average value of all numbers in the chat for a specific user.
Example:

    user1: 14
    average-number-bot: The average of numbers for this channel is: 14.0
    
    user1: 18
    average-number-bot: The average of numbers for this channel is: 16.0
    
    user1: test
    average-number-bot: Hmm.. There is no number/s in your previous message. The last average was: 16.0

Also, this bot will output the average of all numbers people wrote to one of the public channels every minute only if there were any new messages since the last time
Example:

    Channel_1
    user1: 14
    average-number-bot: The average of numbers for this channel is: 14.0
    
    user1: 18
    average-number-bot: The average of numbers for this channel is: 16.0
    
    Channel_2
    user2: 20
    average-number-bot: The average of numbers for this channel is: 20.0
    
    user2: 30
    average-number-bot: The average of numbers for this channel is: 25.0
    
    Public_Channel
    Total average of all numbers in your direct message channels with me is: 18.75
    
Also, there is an API with two routes that returns json response. Routes:

    http://0.0.0.0:5000/average
    Response:
    {
        "average":18.75,
        "message":'Average of all numbers in all direct message channels",
    {
    
    http://0.0.0.0:5000/average/user1
    Response:
    {
        "average":16.0,
        "message":"Average of all numbers for user1 user"
    }

To successfully run a project, the following steps must be completed:

  1. Add next environment variables to your ~/.bashrc file:
  
    export SLACK_TOKEN='xoxb-yourtoken' /bot token
    export PUBLIC_CHANNEL='your-public-channel-id' / one of the public channels id
  
  2. Source ~/.bashrc file
  
    source ~/.bashrc
  
  3. Clone the project with the next command: 
  
    git clone https://github.com/biba-power/slackbot.git
  
  4. Inside projects directory create virtualenv: 
  
    cd slackbot
    virtualenv -p /usr/bin/python3 venv

  5. Activate the venv:
  
    source venv/bin/activate
    
  6. Install requirements:
  
    pip install -r requirements.txt
    
  7. Run tests:
  
    cd average_number_slackbot
    python -m pytest
    
  8. Start run_project.sh script;
  
    cd ../
    ./run_project.sh

After those steps, the API will be available on 0.0.0.0:5000

If you want to test this API, there is a live server on this link http://116.203.190.86:5000/average.
Available users are:
    
    * http://116.203.190.86:5000/average/average.slack.bot
    * http://116.203.190.86:5000/average/average.slack.bot_1
    * http://116.203.190.86:5000/average/average.slack.bot_2
    * http://116.203.190.86:5000/average/average.slack.bot_3
    
  
    
