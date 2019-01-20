from abc import abstractmethod


class MessageAction:

    def __init__(self, config):
        self._config = config

    @staticmethod
    @abstractmethod
    def create(config):
        raise NotImplementedError

    @abstractmethod
    def perform(self, msg):
        raise NotImplementedError
