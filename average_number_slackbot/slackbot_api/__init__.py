from .views import total_average, average

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.register_blueprint(total_average.bp)
    app.register_blueprint(average.bp)
    return app
