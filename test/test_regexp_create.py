import unittest
from mqtt_translator.translator.regexp_translator import RegExpTranslator
from paho.mqtt.client import MQTTMessage


class TestRegExpCreate(unittest.TestCase):

    def test_create_givenRegExpConfig_shouldCopyConfig(self):
        config = {
            'regexp': [{
                'topic_search': 'temp/(auto)',
                'payload_search': r'(heat) (\d+)',
                'topic_template': 'temp/[payload.1]',
                'payload_template': '[payload.2] - [topic.1]',
            }]
        }

        result = RegExpTranslator.create(config)

        self.assertEqual(result._config, config['regexp'])

    def test_create_givenTopicConfig_shouldConvertRegExpConfig(self):
        config = {
            'topic': [{
                'from': 'temp',
                'to': 'heat'
            }]
        }

        result = RegExpTranslator.create(config)

        self.assertEqual(result._config, [
                         {'topic_search': 'temp', 'topic_template': 'heat'}])

    def test_create_givenPayloadConfig_shouldConvertRegExpConfig(self):
        config = {
            'payload': [{
                'from': 'temp',
                'to': 'heat'
            }]
        }

        result = RegExpTranslator.create(config)

        self.assertEqual(result._config, [
                         {'payload_search': 'temp', 'payload_template': 'heat'}])


if __name__ == '__main__':
    unittest.main()
