from slackbot_engine.utils import return_numbers
from slackbot_engine.average_engine import AverageEngine
from slackbot_engine.exceptions import NoNumbersForwarded
import pytest

def test_return_numbers():
    numbers_string = '24 45 89'
    assert return_numbers(numbers_string) == [24.0, 45.0, 89.00]
    numbers_string = 'asd 4 asw 5 dsad 45'
    assert return_numbers(numbers_string) == [4.0, 5.0, 45.00]

def test_string_without_numbers():
    string_without_numbers = 'slackbotslackbotslackbotslackbot'
    with pytest.raises(NoNumbersForwarded):
        assert return_numbers(string_without_numbers)

def test_get_channel_id():
    average_engine = AverageEngine()
    username = 'nemanja.spajic.sa'
    channel = 'DPL0M0PFA'
    assert average_engine.get_channel_id(username) == channel
