from .regexp_translator import RegExpTranslator

class MessageConvertor:

    def __init__(self, config):
        self.__config = config

        self._actions = []
        for configLine in config:
            self._add(RegExpTranslator.create(configLine))

    def _add(self, action):
        if action is not None:
            self._actions.append(action)

    def convert(self, msg):
        for action in self._actions:
            action.perform(msg)
