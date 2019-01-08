from .message_translator_base import MessageTranslatorBase


class TopicPayloadSubstitute(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'topic_payload_subst' in config:
            return TopicPayloadSubstitute(config['topic_payload_subst'])
        else:
            return None

    def translate(self, msg):
        for config in self._config:
            if self._isSameTopicAndPayload(config, msg):
                self._replaceTopicAndPayload(config, msg)

    def _isSameTopicAndPayload(self, config, msg):
        return config['from_topic'] == msg.topic \
            and config['from_payload'] == msg.payload.decode('utf-8')

    def _replaceTopicAndPayload(self, config, msg):
        msg.topic = config['to_topic'].encode('utf-8')
        msg.payload = config['to_payload'].encode('utf-8')