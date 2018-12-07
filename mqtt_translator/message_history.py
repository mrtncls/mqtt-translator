import time

try:
    # Use monotonic clock if available
    time_func = time.monotonic
except AttributeError:
    time_func = time.time

class MessageHistory:

    def __init__(self, validtTimespanSec):
        self.__history = {}
        self.__validTimespanSec = validtTimespanSec

    def __isvalid(self, hash):
        return \
            hash in self.__history \
            and self.__history[hash] > time_func() - self.__validTimespanSec

    def has_message(self, hash):
        return self.__isvalid(hash)

    def add_message(self, hash):
        self.__history[hash] = time_func()

    def purge(self):
        for key in list(self.__history):
            if (self.__history[key] < time_func() - self.__validTimespanSec):
                del self.__history[key]
