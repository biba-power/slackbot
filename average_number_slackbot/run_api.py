from slackbot_api import create_app

if __name__ == '__main__':
    """
    Python script that will run Flask application on 0.0.0.0:5000
    """
    app = create_app()
    app.run()