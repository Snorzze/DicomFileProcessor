__author__ = 'Max'


class ShiftError(Exception):
    def __init__(self, arg):
        # Set some exception infomation
        self.msg = arg
