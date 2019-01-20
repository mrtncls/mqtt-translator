import unittest
from mqtt_translator.translator.message_convertor import MessageConvertor
from paho.mqtt.client import MQTTMessage


class TestMessageConvertor(unittest.TestCase):

    def test_convert_givenConfigRegExp_shouldUseRegExp(self):
        config = [{
            'regexp': [
                {
                    'topic_search': 'temp/(auto)',
                    'payload_search': r'(heat) (\d+)',
                    'topic_template': 'temp/[payload.1]',
                    'payload_template': '[payload.2] - [topic.1]',
                }
            ]
        }]
        convertor = MessageConvertor(config)
        message = MQTTMessage()
        message.topic = 'my/test/temp/auto'.encode('utf-8')
        message.payload = 'heat 99'.encode('utf-8')        

        convertor.convert(message)

        self.assertEqual(message.topic, 'my/test/temp/heat')
        self.assertEqual(message.payload, '99 - auto'.encode('utf-8'))

    def test_convert_givenConfigTopic_shouldUseRegExp(self):
        config = [{
            'topic': [
                {
                    'from': 'you',
                    'to': 'me'
                }
            ]
        }]
        convertor = MessageConvertor(config)
        message = MQTTMessage()
        message.topic = 'my/test/for/you'.encode('utf-8')

        convertor.convert(message)

        self.assertEqual(message.topic, 'my/test/for/me')

    def test_convert_givenConfigPayload_shouldUseRegExp(self):
        config = [{
            'payload': [
                {
                    'from': 'you',
                    'to': 'me'
                }
            ]
        }]
        convertor = MessageConvertor(config)
        message = MQTTMessage()
        message.payload = 'you'.encode('utf-8')

        convertor.convert(message)

        self.assertEqual(message.payload, 'me'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
