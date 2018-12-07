import unittest
from mqtt_translator.topic_translator import TopicTranslator

class TestTopicTranslator(unittest.TestCase):

    def test_translate_given2configitems_shouldtranslate(self):
        config = [
            { 'from': 'xyz', 'to': '123' },
            { 'from': 'home', 'to': 'away' }
        ]
        translator = TopicTranslator(config)

        result = translator.translate('home xyz')
        
        self.assertEqual(result, 'away 123')

    def test_translate_given2overlappingconfigitems_shouldtranslateinorder(self):
        config = [
            { 'from': 'xyz', 'to': '123' },
            { 'from': '123', 'to': 'zyx' }
        ]
        translator = TopicTranslator(config)

        result = translator.translate('xyz')
        
        self.assertEqual(result, 'zyx')

if __name__ == '__main__':
    unittest.main()