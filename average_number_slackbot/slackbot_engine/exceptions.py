class NoNumbersForwarded(Exception):
    """Raised when message does not contain number/s"""
    pass


class NotPrivateChannel(Exception):
    """Raised when channel is not private"""
    pass


class MemberDoesNotExist(Exception):
    """Raised when a member with input username does not exist in the slack team"""
    pass


class MemberDoesNotHaveDmc(Exception):
    """Raised when a member does not have private channel with Bot"""
    pass


class NoMessagesInChannel(Exception):
    """Raised when the length of messages in the channel is equal to 0"""
    pass
