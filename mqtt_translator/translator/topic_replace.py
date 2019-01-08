from .message_translator_base import MessageTranslatorBase


class TopicReplace(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'topic_replace' in config:
            return TopicReplace(config['topic_replace'])
        else:
            return None

    def translate(self, msg):
        topic = msg.topic
        for topic_replace in self._config:
            topic = topic.replace(topic_replace['from'], topic_replace['to'])

        msg.topic = topic.encode('utf-8')

