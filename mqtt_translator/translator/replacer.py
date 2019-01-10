from .message_translator_base import MessageTranslatorBase


class Replacer(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'replace' in config:
            return Replacer(config['replace'])
        else:
            return None

    def translate(self, msg):
        for config in self._config:
            if self._isMatching(config, msg):
                self._replaceTopicAndPayload(config, msg)

    def _isMatching(self, config, msg):
        if 'topic' in config and 'payload' in config:
            return self._isSameTopicAndPayload(config, msg)
        elif 'topic' in config:
            return self._isSameTopic(config, msg)
        elif 'payload' in config:
            return self._isSamePayload(config, msg)
        else:
            raise InvalidConfigException("Topic or payload is required")

    def _isSameTopic(self, config, msg):
        return config['topic'] == msg.topic

    def _isSamePayload(self, config, msg):
        return config['payload'] == msg.payload.decode('utf-8')

    def _isSameTopicAndPayload(self, config, msg):
        return self._isSameTopic(config, msg) and self._isSamePayload(config, msg)

    def _replaceTopicAndPayload(self, config, msg):
        if 'new_topic' in config:
            msg.topic = config['new_topic'].encode('utf-8')
        if 'new_payload' in config:
            msg.payload = config['new_payload'].encode('utf-8')


class InvalidConfigException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
