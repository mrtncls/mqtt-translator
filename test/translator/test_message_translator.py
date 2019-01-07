import unittest
from mqtt_translator.translator.message_translator import MessageTranslator
from paho.mqtt.client import MQTTMessage


class TestMessageTranslator(unittest.TestCase):

    def test_translate_givenconfigwithtranslatortopicsection_shouldusetopictranslator(self):
        config = {
            'topic': [
                {'from': 'home', 'to': 'away'}
            ]
        }
        translator = MessageTranslator(config)
        message = MQTTMessage()
        message.topic = 'home'.encode('utf-8')

        result = translator.translate(message)

        self.assertEqual(result.topic, 'away')


if __name__ == '__main__':
    unittest.main()
