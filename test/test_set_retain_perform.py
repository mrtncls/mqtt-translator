import unittest
from mqtt_translator.translator.set_retain import SetRetain
from paho.mqtt.client import MQTTMessage


class TestSetRetainCreate(unittest.TestCase):

    def setUp(self):
        self.message = MQTTMessage()
        self.message.topic = 'my/test/topic'.encode('utf-8')
        self.message.retain = False
        self.config = [
            {
                'topic_fullmatch': '.*topic',
                'retain': True
            }
        ]

    def test_perform_givenMatch_shouldSet(self):
        translator = SetRetain(self.config)

        translator.perform(self.message)

        self.assertTrue(self.message.retain)

    def test_perform_givenMatchResetRetain_shouldSet(self):
        self.message.retain = True
        self.config[0]['retain'] = False
        translator = SetRetain(self.config)

        translator.perform(self.message)

        self.assertFalse(self.message.retain)

    def test_perform_givenConfigWithoutSearch_shouldSet(self):
        del self.config[0]['topic_fullmatch']
        translator = SetRetain(self.config)

        translator.perform(self.message)

        self.assertTrue(self.message.retain)

    def test_perform_givenNoMatch_shouldNotSet(self):
        self.config[0]['topic_fullmatch'] = 'house'
        translator = SetRetain(self.config)

        translator.perform(self.message)

        self.assertFalse(self.message.retain)


if __name__ == '__main__':
    unittest.main()
