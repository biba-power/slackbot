from flask import Blueprint
from average_number_slackbot.slackbot_engine.average_engine import AverageEngine

bp = Blueprint('average', __name__)

@bp.route('/average', methods=['GET'])
def average(username):

    average_engine = AverageEngine()
    average_data = average_engine.get_data_for_all_channels()
    total_average = round(average_data['total_sum'] / average_data['total_count'],2)
    return 'Average data for all channels is {0}'.format(total_average)