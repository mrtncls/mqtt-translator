from .payload_replace import PayloadReplace
from .topic_replace import TopicReplace
from .topic_payload_substitute import TopicPayloadSubstitute


class MessageTranslator:

    def __init__(self, config):
        self.__config = config

        self._translators = []
        self._add(PayloadReplace.create(config))
        self._add(TopicReplace.create(config))
        self._add(TopicPayloadSubstitute.create(config))

    def _add(self, translator):
        if translator is not None:
            self._translators.append(translator)

    def translate(self, msg):
        for translator in self._translators:
            translator.translate(msg)
