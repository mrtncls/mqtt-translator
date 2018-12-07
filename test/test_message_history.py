import unittest
import time
from mqtt_translator.message_history import MessageHistory

class TestMessageHistory(unittest.TestCase):

    def test_has_message(self):
        messageHistory = MessageHistory(2)
        messageHistory.add_message(1)

        result = messageHistory.has_message(1)

        self.assertEqual(result, True)

    def test_add_message(self):
        messageHistory = MessageHistory(2)

        messageHistory.add_message(1)
        result = messageHistory.has_message(1)

        self.assertEqual(result, True)

    def test_purge(self):
        messageHistory = MessageHistory(2)
        messageHistory.add_message(1)
        time.sleep(1)
        messageHistory.add_message(2)
        time.sleep(1)
        messageHistory.add_message(3)
        
        messageHistory.purge()
        hasMessage1 = messageHistory.has_message(1)
        hasMessage2 = messageHistory.has_message(2)
        hasMessage3 = messageHistory.has_message(3)

        self.assertEqual(hasMessage1, False)
        self.assertEqual(hasMessage2, True)
        self.assertEqual(hasMessage3, True)

if __name__ == '__main__':
    unittest.main()