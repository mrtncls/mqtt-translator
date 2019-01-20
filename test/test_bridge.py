import unittest
import time
from mqtt_translator.bridge import Bridge


class TestBridge(unittest.TestCase):

    def __init__(self, methodName='runTest'):

        self.valid_config = {
            'source': {
                'id': 'source_test',
                'host': 'source_host',
                'port': 123,
                'keepalive_interval': 5,
                'topics': ['source_topic'],
                'publish': {
                    'cooldown': 2,
                    'convert': {}
                }
            },
            'target': {
                'id': 'target_test',
                'host': 'target_host',
                'port': 123,
                'keepalive_interval': 5,
                'topics': ['target_topic'],
                'publish': {
                    'cooldown': 2,
                    'convert': {}
                }
            }
        }

        self.invalid_config = {
            'source': {
                'id': 'source_test',
            },
            'target': {
                'id': 'target_test',
            }
        }

        super().__init__(methodName=methodName)

    def test_init_withvalidconfig_shouldnotthrow(self):

        Bridge(self.valid_config)

    def test_init_withinvalidvalidconfig_shouldthrow(self):

        self.assertRaises(Exception, Bridge, self.invalid_config)

    def test_init_shouldcreatebridge(self):

        bridge = Bridge(self.valid_config)

        self.assertEqual(bridge._source._other_bridge_client, bridge._target)
        self.assertEqual(bridge._target._other_bridge_client, bridge._source)


if __name__ == '__main__':
    unittest.main()
