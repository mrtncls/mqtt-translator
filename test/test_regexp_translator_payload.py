import unittest
from mqtt_translator.translator.regexp_translator import RegExpTranslator
from paho.mqtt.client import MQTTMessage


class TestRegExpTranslatorPayload(unittest.TestCase):

    def setUp(self):
        self.message = MQTTMessage()
        self.message.payload = 'payload 99'.encode('utf-8')
        self.config = [
            {
                'payload_search': r'payload (\d+)',
                'payload_template': 'Temperature is [payload.1]',
            }
        ]

    def test_translate_givenSearchWithMatch_shouldRender(self):
        translator = RegExpTranslator(self.config)

        translator.translate(self.message)

        self.assertEqual(self.message.payload,
                         'Temperature is 99'.encode('utf-8'))

    def test_translate_givenReplaceConfig_shouldRender(self):
        translator = RegExpTranslator([
            {
                'payload_search': '99',
                'payload_template': '88',
            }
        ])

        translator.translate(self.message)

        self.assertEqual(self.message.payload, 'payload 88'.encode('utf-8'))

    def test_translate_givenSearchButNoMatch_shouldNotRender(self):
        self.config[0]['payload_search'] = r'daolyap (\d+)'
        translator = RegExpTranslator(self.config)

        translator.translate(self.message)

        self.assertEqual(self.message.payload,
                         'payload 99'.encode('utf-8'))

    def test_translate_givenNoSearchInConfig_shouldNotRender(self):
        del self.config[0]['payload_search']
        translator = RegExpTranslator(self.config)

        translator.translate(self.message)

        self.assertEqual(self.message.payload,
                         'payload 99'.encode('utf-8'))

    def test_translate_givenOutOfRangeIndex_shouldRaise(self):
        self.config[0]['payload_template'] = 'Temperature is [payload.987]'
        translator = RegExpTranslator(self.config)

        with self.assertRaises(Exception):
            translator.translate(self.message)

    def test_translate_givenSearchWithoutGroupButVarInTemplate_shouldRaise(self):
        self.config[0]['payload_search'] = 'payload'
        translator = RegExpTranslator(self.config)

        with self.assertRaises(Exception):
            translator.translate(self.message)

    def test_translate_givenNoTemplate_shouldNotRender(self):
        del self.config[0]['payload_template']
        translator = RegExpTranslator(self.config)

        translator.translate(self.message)

        self.assertEqual(self.message.payload,
                         'payload 99'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
