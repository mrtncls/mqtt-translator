from .topic_translator import TopicTranslator


class MessageTranslator:

    def __init__(self, config):
        self.__config = config

        self._translators = []
        self._add(TopicTranslator.create(config))

    def _add(self, translator):
        if translator is not None:
            self._translators.append(translator)

    def translate(self, msg):
        for translator in self._translators:
            msg = translator.translate(msg)
        return msg
