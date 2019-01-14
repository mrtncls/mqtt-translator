import unittest
from mqtt_translator.translator.message_translator import MessageTranslator
from paho.mqtt.client import MQTTMessage


class TestMessageTranslator(unittest.TestCase):

    def test_translate_givenConfigRegExp_shouldUseRegExp(self):
        config = {
            'regexp': [
                {
                    'topic_search': 'temp/(auto)',
                    'payload_search': r'(heat) (\d+)',
                    'topic_template': 'temp/[payload.1]',
                    'payload_template': '[payload.2] - [topic.1]',
                }
            ]
        }
        translator = MessageTranslator(config)
        message = MQTTMessage()
        message.topic = 'my/test/temp/auto'.encode('utf-8')
        message.payload = 'heat 99'.encode('utf-8')        

        translator.translate(message)

        self.assertEqual(message.topic, 'my/test/temp/heat')
        self.assertEqual(message.payload, '99 - auto'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
