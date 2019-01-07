from .message_translator_base import MessageTranslatorBase


class TopicTranslator(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'topic' in config:
            return TopicTranslator(config['topic'])
        else:
            return None

    def translate(self, msg):
        topic = msg.topic
        for topic_replace in self._config:
            topic = topic.replace(topic_replace['from'], topic_replace['to'])

        msg.topic = topic.encode('utf-8')
        return msg

