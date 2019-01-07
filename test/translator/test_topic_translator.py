import unittest
from mqtt_translator.translator.topic_translator import TopicTranslator
from paho.mqtt.client import MQTTMessage


class TestTopicTranslator(unittest.TestCase):

    def test_translate_given2configitems_shouldtranslate(self):
        config = [
            {'from': 'xyz', 'to': '123'},
            {'from': 'home', 'to': 'away'}
        ]
        translator = TopicTranslator(config)
        message = MQTTMessage()
        message.topic = 'home xyz'.encode('utf-8')

        result = translator.translate(message)

        self.assertEqual(result.topic, 'away 123')

    def test_translate_given2overlappingconfigitems_shouldtranslateinorder(self):
        config = [
            {'from': 'xyz', 'to': '123'},
            {'from': '123', 'to': 'zyx'}
        ]
        translator = TopicTranslator(config)
        message = MQTTMessage()
        message.topic = 'xyz'.encode('utf-8')

        result = translator.translate(message)

        self.assertEqual(result.topic, 'zyx')


if __name__ == '__main__':
    unittest.main()
