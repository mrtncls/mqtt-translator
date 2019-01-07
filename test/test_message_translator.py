import unittest
from mqtt_translator.translator.message_translator import MessageTranslator
from paho.mqtt.client import MQTTMessage


class TestMessageTranslator(unittest.TestCase):

    def test_translate_givenconfigwithtranslatortopicsection_shouldusetopictranslator(self):
        config = {
            'topicReplace': [
                {'from': 'home', 'to': 'away'}
            ]
        }
        translator = MessageTranslator(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.topic, 'away')

    def test_translate_givenconfigwithtranslatortopicpayloadsection_shouldusetopicpayloadtranslator(self):
        config = {
            'topicPayloadSubstitute': [
                {
                    'from_topic': 'home',
                    'from_payload': '50',
                    'to_topic': 'state',
                    'to_payload': 'home50'
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
