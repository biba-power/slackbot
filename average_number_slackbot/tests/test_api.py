import pytest
from slackbot_api import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_average_status_code(client):
    response = client.get("/average")
    assert response.status_code == 200

def test_useraverage_status_code(client):
    response = client.get("/average/nemanja.spajic.sa")
    assert response.status_code == 200

def test_wrong_username(client):
    response = client.get("/average/this_name_should_never_be_used")
    assert response.status_code == 404