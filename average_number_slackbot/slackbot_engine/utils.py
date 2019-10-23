from .exceptions import NoNumbersForwarded

def return_numbers(in_message):
    '''
    Method that returns list of numbers from string message
    :param in_message: message from slack
    :return: list of numbers if everything is ok, otherwise raise NoNumbersProvided exception
    '''
    words_list = in_message.split(' ')
    numbers = []
    for word in words_list:
        try:
            numbers.append(float(word))
        except ValueError:
            pass

    if len(numbers)<1:
        raise NoNumbersForwarded
    return numbers