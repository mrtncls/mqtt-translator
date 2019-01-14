import re
import copy
from .message_translator_base import MessageTranslatorBase


class RegExpTranslator(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'regexp' in config:
            return RegExpTranslator(config['regexp'])
        elif 'topic' in config:
            topicConfig = copy.deepcopy(config['topic'])
            RegExpTranslator._convertTopicConfigToRegExpConfig(topicConfig)
            return RegExpTranslator(topicConfig)
        elif 'payload' in config:
            payloadConfig = copy.deepcopy(config['payload'])
            RegExpTranslator._convertPayloadConfigToRegExpConfig(payloadConfig)
            return RegExpTranslator(payloadConfig)
        else:
            return None

    @staticmethod
    def _convertTopicConfigToRegExpConfig(config):
        for topicConfig in config:
            topicConfig['topic_search'] = topicConfig.pop('from')
            topicConfig['topic_template'] = topicConfig.pop('to')

    @staticmethod
    def _convertPayloadConfigToRegExpConfig(config):
        for payloadConfig in config:
            payloadConfig['payload_search'] = payloadConfig.pop('from')
            payloadConfig['payload_template'] = payloadConfig.pop('to')

    def translate(self, msg):
        for config in self._config:
            topic_match = self._matchTopic(config, msg)
            payload_match = self._matchPayload(config, msg)

            if not self._hasMatch(config, topic_match, payload_match):
                continue

            if 'topic_template' in config:
                template = self._getTopicTemplate(config, msg)
                msg.topic = self._render(topic_match, payload_match, template)

            if 'payload_template' in config:
                template = self._getPayloadTemplate(config, msg)
                msg.payload = self._render(topic_match, payload_match, template)

    def _matchTopic(self, config, msg):
        if 'topic_search' in config:
            return re.search(config['topic_search'], msg.topic)
        return None

    def _matchPayload(self, config, msg):
        if 'payload_search' in config:
            return re.search(config['payload_search'], msg.payload.decode('utf-8'))
        return None

    def _hasMatch(self, config, topic_match, payload_match):
        return (topic_match or payload_match) \
            and (topic_match or 'topic_search' not in config) \
            and (payload_match or 'payload_search' not in config)

    def _getTopicTemplate(self, config, msg):
        if 'topic_search' in config:
            return re.sub(config['topic_search'], config['topic_template'], msg.topic)
        return config['topic_template']

    def _getPayloadTemplate(self, config, msg):
        if 'payload_search' in config:
            return re.sub(config['payload_search'], config['payload_template'], msg.payload.decode('utf-8'))
        return config['payload_template']

    def _render(self, topic_match, payload_match, template):
        result = template
        if topic_match:
            result = self._renderTopic(topic_match, result)
        if payload_match:
            result = self._renderPayload(payload_match, result)
        return result.encode('utf-8')

    def _renderTopic(self, topic_match, template):
        result = template
        for match in re.finditer(r'\[topic\.(\d+)\]', result):
            index = int(match.group(1))
            result = re.sub(rf'\[topic\.{index}\]', topic_match.group(index), result)
        return result

    def _renderPayload(self, payload_match, template):
        result = template
        for match in re.finditer(r'\[payload\.(\d+)\]', result):
            index = int(match.group(1))
            result = re.sub(rf'\[payload\.{index}\]', payload_match.group(index), result)
        return result