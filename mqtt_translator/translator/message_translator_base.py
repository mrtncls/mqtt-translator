from abc import abstractmethod


class MessageTranslatorBase:

    def __init__(self, config):
        self._config = config

    @staticmethod
    @abstractmethod
    def create(config):
        raise NotImplementedError

    @abstractmethod
    def translate(self, msg):
        raise NotImplementedError

