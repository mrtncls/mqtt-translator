import unittest
from mqtt_translator.translator.payload_replace import PayloadReplace
from paho.mqtt.client import MQTTMessage


class TestPayloadReplace(unittest.TestCase):

    def test_translate_givenMatchingConfig_shouldTranslate(self):
        config = [
            {'from': 'automatic', 'to': 'heat'}
        ]
        translator = PayloadReplace(config)
        message = MQTTMessage()
        message.payload = 'home automatic mode'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.payload, 'home heat mode'.encode('utf-8'))

    def test_translate_giveNotMatchingConfig_shouldNotTranslate(self):
        config = [
            {'from': 'automatic', 'to': 'heat'}
        ]
        translator = PayloadReplace(config)
        message = MQTTMessage()
        message.payload = 'baby G'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.payload, 'baby G'.encode('utf-8'))

    def test_translate_givenTwoMatchingConfigs_shouldTranslateInOrder(self):
        config = [
            {'from': 'automatic', 'to': 'heat'},
            {'from': 'heat', 'to': 'heating'}
        ]
        translator = PayloadReplace(config)
        message = MQTTMessage()
        message.payload = 'home automatic mode'.encode('utf-8')

        translator.translate(message)

        self.assertEqual(message.payload, 'home heating mode'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
