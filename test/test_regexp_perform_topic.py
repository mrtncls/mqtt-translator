import unittest
from mqtt_translator.translator.regexp_translator import RegExpTranslator
from paho.mqtt.client import MQTTMessage


class TestRegExpPerformTopic(unittest.TestCase):

    def setUp(self):
        self.message = MQTTMessage()
        self.message.topic = 'my/test/topic'.encode('utf-8')
        self.config = [
            {
                'topic_search': '(topic)',
                'topic_template': 'Your [topic.1] is my [topic.1]',
            }
        ]

    def test_perform_givenSearchWithMatch_shouldRender(self):
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/Your topic is my topic')

    def test_perform_givenReplaceConfig_shouldRender(self):
        translator = RegExpTranslator([
            {
                'topic_search': 'topic',
                'topic_template': 'case',
            }
        ])

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/case')

    def test_perform_givenSearchButNoMatch_shouldNotRender(self):
        self.config[0]['topic_search'] = '(cipot)'
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/topic')

    def test_perform_givenNoSearchInConfig_shouldNotRender(self):
        del self.config[0]['topic_search']
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/topic')

    def test_perform_givenOutOfRangeIndex_shouldRaise(self):
        self.config[0]['topic_template'] = 'Your [topic.654]'
        translator = RegExpTranslator(self.config)

        with self.assertRaises(Exception):
            translator.perform(self.message)

    def test_perform_givenSearchWithoutGroupButVarInTemplate_shouldRaise(self):
        self.config[0]['topic_search'] = 'topic'
        translator = RegExpTranslator(self.config)

        with self.assertRaises(Exception):
            translator.perform(self.message)

    def test_perform_givenNoTemplate_shouldNotRender(self):
        del self.config[0]['topic_template']
        translator = RegExpTranslator(self.config)

        translator.perform(self.message)

        self.assertEqual(self.message.topic, 'my/test/topic')


if __name__ == '__main__':
    unittest.main()
