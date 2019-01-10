from .replacer import Replacer


class MessageTranslator:

    def __init__(self, config):
        self.__config = config

        self._translators = []
        self._add(Replacer.create(config))

    def _add(self, translator):
        if translator is not None:
            self._translators.append(translator)

    def translate(self, msg):
        for translator in self._translators:
            translator.translate(msg)
