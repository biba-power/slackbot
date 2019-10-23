from flask import Blueprint
from slackbot_engine.average_engine import AverageEngine
from flask import jsonify
from slackbot_engine.exceptions import MemberDoesNotHaveDmc, MemberDoesNotExist, \
    NoMessagesInChannel

bp = Blueprint('average', __name__)


@bp.route('/average/<username>', methods=['GET'])
def average(username):
    try:
        average_engine = AverageEngine()
        channel_id = average_engine.get_channel_id(username)
        channel_data = average_engine.get_data_for_channel(channel_id)
        total_average = round(channel_data['numbers_sum'] / channel_data['numbers_count'], 2)
        return_dict = {'message': 'Average of all numbers for {0} user'.format(username), 'average': total_average}
        return jsonify(return_dict)
    except MemberDoesNotExist as mdne:
        return jsonify(error=404, text=str(mdne)), 404

    except MemberDoesNotHaveDmc as mdnhd:
        return jsonify(error=404, text=str(mdnhd)), 404

    except NoMessagesInChannel as nmic:
        return jsonify(error=404, text=str(nmic)), 404

