import unittest
from mqtt_translator.translator.topic_payload_substitute import TopicPayloadSubstitute
from paho.mqtt.client import MQTTMessage


class TestTopicPayloadSubstitute(unittest.TestCase):

    def test_translate_given2configitems_shouldtranslate(self):
        config = [
            {
                'from_topic': 'home',
                'from_payload': '50',
                'to_topic': 'state',
                'to_payload': 'home50'
            },
            {
                'from_topic': 'home',
                'from_payload': '60',
                'to_topic': 'state',
                'to_payload': 'home60'
            }
        ]
        translator = TopicPayloadSubstitute(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'state')
        self.assertEqual(message.payload, 'home60'.encode('utf-8'))

    def test_translate_givennotmatchingconfigitems_shouldnottranslate(self):
        config = [
            {
                'from_topic': 'home',
                'from_payload': '50',
                'to_topic': 'state',
                'to_payload': 'home50'
            },
            {
                'from_topic': 'home',
                'from_payload': '70',
                'to_topic': 'state',
                'to_payload': 'home70'
            }
        ]
        translator = TopicPayloadSubstitute(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')
        message.payload = '60'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'home')
        self.assertEqual(message.payload, '60'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
