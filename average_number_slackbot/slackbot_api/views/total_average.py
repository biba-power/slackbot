from flask import Blueprint
from slackbot_engine.average_engine import AverageEngine
from flask import jsonify

bp = Blueprint('total_average', __name__)


@bp.route('/average', methods=['GET'])
def average():
    average_engine = AverageEngine()
    average_data = average_engine.get_data_for_all_channels()
    total_average = round(average_data['total_sum'] / average_data['total_count'], 2)
    return_dict = {'message': 'Average of all numbers in all direct message channels', 'average': total_average}
    return jsonify(return_dict)
