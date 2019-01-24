import unittest
from mqtt_translator.translator.regexp_translator import RegExpTranslator
from paho.mqtt.client import MQTTMessage


class TestRegExpPerform(unittest.TestCase):

    def setUp(self):
        self.message = MQTTMessage()
        self.message.topic = 'my/test/temp/auto'.encode('utf-8')
        self.message.payload = 'heat 99'.encode('utf-8')
        self.config = [
            {
                'topic_search': 'temp/(auto)',
                'payload_search': r'(heat) (\d+)',
                'topic_template': 'temp/[payload.1]',
                'payload_template': '[payload.2] - [topic.1]'
            }
        ]

    def test_perform_givenEmptyPayloadTemplate_shouldRender(self):
        self.config = [
            {
                'topic_search': '(huis/.*)/thermostaat/set_mode',
                'payload_search': 'dry',
                'topic_template': '[topic.1]/boost',
                'payload_template': ''
            }
        ]
        translator = RegExpTranslator(self.config)
        self.message = MQTTMessage()
        self.message.topic = 'huis/berging_bureau/thermostaat/set_mode'.encode('utf-8')
        self.message.payload = 'dry'.encode('utf-8')

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'huis/berging_bureau/boost')
        self.assertEqual(self.message.payload, ''.encode('utf-8'))

    def test_perform_givenSearchWithMatch_shouldRender(self):
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/temp/heat')
        self.assertEqual(self.message.payload, '99 - auto'.encode('utf-8'))

    def test_perform_givenNoTopicSearchButTopicTemplate_shouldRender(self):
        del self.config[0]['topic_search']
        self.config[0]['payload_template'] = '[payload.2]'
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'temp/heat')
        self.assertEqual(self.message.payload, '99'.encode('utf-8'))

    def test_perform_givenNoPayloadSearchButPayloadTemplate_shouldRender(self):
        del self.config[0]['payload_search']
        self.config[0]['topic_template'] = 'temp/[topic.1]'
        self.config[0]['payload_template'] = '[topic.1]'
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/temp/auto')
        self.assertEqual(self.message.payload, 'auto'.encode('utf-8'))

    def test_perform_givenMultipleConfigs_shouldTranslateInOrder(self):
        self.config = [
            {
                'topic_search': 'temp/(auto)',
                'payload_search': r'(heat) (\d+)',
                'topic_template': 'temp/[payload.1]',
                'payload_template': '[payload.2] - [topic.1]'
            },
            {
                'topic_search': 'temp/(heat)',
                'payload_search': r'(\d+).*',
                'topic_template': '[topic.1]',
                'payload_template': '[payload.1]'
            }
        ]        
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/heat')
        self.assertEqual(self.message.payload, '99'.encode('utf-8'))

    def test_perform_givenMatchAndNoMatchConfig_shouldTranslate(self):
        self.config = [
            {
                'topic_search': 'ppp',
                'payload_search': 'rrr',
                'topic_template': 'lll',
                'payload_template': 'kkk'
            },
            {
                'topic_search': 'temp/(auto)',
                'payload_search': r'(heat) (\d+)',
                'topic_template': 'temp/[payload.1]',
                'payload_template': '[payload.2] - [topic.1]'
            }
        ]        
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/temp/heat')
        self.assertEqual(self.message.payload, '99 - auto'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
