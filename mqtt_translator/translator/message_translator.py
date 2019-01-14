from .regexp_translator import RegExpTranslator

class MessageTranslator:

    def __init__(self, config):
        self.__config = config

        self._translators = []
        for configLine in config:
            self._add(RegExpTranslator.create(configLine))

    def _add(self, translator):
        if translator is not None:
            self._translators.append(translator)

    def translate(self, msg):
        for translator in self._translators:
            translator.translate(msg)
