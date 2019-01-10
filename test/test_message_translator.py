import unittest
from mqtt_translator.translator.message_translator import MessageTranslator
from paho.mqtt.client import MQTTMessage


class TestMessageTranslator(unittest.TestCase):

    def test_translate_givenConfigReplacer_shouldUseReplacer(self):
        config = {
            'replace': [
                {
                    'topic': 'home',
                    'payload': '50',
                    'new_topic': 'state',
                    'new_payload': 'home50'
                }
            ]
        }
        translator = MessageTranslator(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '50'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'state')
        self.assertEqual(message.payload, 'home50'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
