import unittest
from mqtt_translator.translator.replacer import Replacer, InvalidConfigException
from paho.mqtt.client import MQTTMessage


class TestReplacer(unittest.TestCase):

    def test_translate_givenMatchingTopicAndPayload_shouldTranslateTopicAndPayload(self):
        config = [
            {
                'topic': 'home',
                'payload': '60',
                'new_topic': 'state',
                'new_payload': 'home60'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'state')
        self.assertEqual(message.payload, 'home60'.encode('utf-8'))

    def test_translate_givenMatchingTopicAndPayload_shouldTranslateTopic(self):
        config = [
            {
                'topic': 'home',
                'payload': '60',
                'new_topic': 'away'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'away')
        self.assertEqual(message.payload, '60'.encode('utf-8'))

    def test_translate_givenMatchingTopicAndPayload_shouldTranslatePayload(self):
        config = [
            {
                'topic': 'home',
                'payload': '60',
                'new_payload': '77'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'home')
        self.assertEqual(message.payload, '77'.encode('utf-8'))

    def test_translate_givenNotMatchingTopicAndPayload_shouldNotTranslate(self):
        config = [
            {
                'topic': 'home',
                'payload': '50',
                'new_topic': 'state',
                'new_payload': 'home50'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'home')
        self.assertEqual(message.payload, '60'.encode('utf-8'))

    def test_translate_givenNotMatchingTopic_shouldNotTranslate(self):
        config = [
            {
                'topic': 'home',
                'new_topic': 'state',
                'new_payload': 'home50'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'here'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'here')
        self.assertEqual(message.payload, '60'.encode('utf-8'))

    def test_translate_givenNotMatchingPayload_shouldNotTranslate(self):
        config = [
            {
                'payload': '55',
                'new_topic': 'state',
                'new_payload': '99'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'there'.encode('utf-8')
        message.payload = '55'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'state')
        self.assertEqual(message.payload, '99'.encode('utf-8'))

    def test_translate_givenTwoMatchingTopicsAndPayloads_shouldTranslateInOrder(self):
        config = [
            {
                'topic': 'home',
                'payload': '60',
                'new_topic': 'away',
                'new_payload': '70'
            },
            {
                'topic': 'away',
                'payload': '70',
                'new_topic': 'gone',
                'new_payload': '80'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'gone')
        self.assertEqual(message.payload, '80'.encode('utf-8'))

    def test_translate_givenMatchingTopic_shouldTranslate(self):
        config = [
            {
                'topic': 'home',
                'new_topic': 'away',
                'new_payload': '70'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'away')
        self.assertEqual(message.payload, '70'.encode('utf-8'))

    def test_translate_givenMatchingPayload_shouldTranslate(self):
        config = [
            {
                'payload': '55',
                'new_topic': 'away',
                'new_payload': '70'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '55'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'away')
        self.assertEqual(message.payload, '70'.encode('utf-8'))

    def test_translate_givenInvalidConfig_shouldRaise(self):
        config = [
            {
                'new_topic': 'away',
                'new_payload': '70'
            }
        ]
        translator = Replacer(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '55'.encode('utf-8')

        with self.assertRaises(InvalidConfigException):
            translator.translate(message)


if __name__ == '__main__':
    unittest.main()
