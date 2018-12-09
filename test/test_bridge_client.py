import time
import unittest
from unittest.mock import Mock, call
from mqtt_translator.bridge_client import BridgeClient
from mqtt_translator.paho_mqtt_client import PahoMqttClient
from paho.mqtt.client import MQTTMessage

class TestBridgeClient(unittest.TestCase):

    def __init__(self, methodName='runTest'):

        self.topics = ['topic1', 'topic2']
        self.topic_translator_config = [
            { 'from': 'xyz', 'to': '123' },
            { 'from': 'home', 'to': 'away' }
        ]

        super().__init__(methodName=methodName)


    def test_id(self):

        mocked_client = Mock(spec=PahoMqttClient)
        mocked_client.id = '123'

        bridge_client = BridgeClient(mocked_client, self.topics, 2, self.topic_translator_config)

        self.assertEquals(bridge_client.id, '123')


    def test_connected_shouldsubscribetotopics(self):

        mocked_client = Mock(spec=PahoMqttClient)
        mocked_client.id = '123'
        bridge_client = BridgeClient(mocked_client, self.topics, 2, self.topic_translator_config)

        bridge_client.connected()

        calls = [call('topic1'), call('topic2')]
        mocked_client.subscribe.assert_has_calls(calls)


    def test_received_shouldpublishonotherclient(self):

        source_mocked_client = Mock(spec=PahoMqttClient)
        source_mocked_client.id = '123'
        source_client = BridgeClient(source_mocked_client, self.topics, 2, self.topic_translator_config)
        target_mocked_client = Mock(spec=PahoMqttClient)
        target_mocked_client.id = '456'
        target_client = BridgeClient(target_mocked_client, self.topics, 2, self.topic_translator_config)
        source_client.bridge(target_client)
        msg = MQTTMessage(topic='test_topic'.encode('utf-8'))
        msg.payload = 'test_payload'
        msg.qos = 0
        msg.retain = True

        source_client.received(msg)

        target_mocked_client.publish.assert_called_once_with('test_topic', payload='test_payload', qos=0, retain=True)


    def test_givenpublishedmessageechoedwithincooldownperiod_shouldnotpublishagain(self):

        source_mocked_client = Mock(spec=PahoMqttClient)
        source_mocked_client.id = '123'
        source_client = BridgeClient(source_mocked_client, self.topics, 2, self.topic_translator_config)
        target_mocked_client = Mock(spec=PahoMqttClient)
        target_mocked_client.id = '456'
        target_client = BridgeClient(target_mocked_client, self.topics, 2, self.topic_translator_config)
        source_client.bridge(target_client)
        target_client.bridge(source_client)
        msg = MQTTMessage(topic='test_topic'.encode('utf-8'))
        msg.payload = 'test_payload'
        msg.qos = 0
        msg.retain = True

        target_client.received(msg)
        source_client.received(msg)

        source_mocked_client.publish.assert_called_once()
        target_mocked_client.publish.assert_not_called()

    def test_givenpublishedmessageechoedaftercooldownperiod_shouldpublishagain(self):

        source_mocked_client = Mock(spec=PahoMqttClient)
        source_mocked_client.id = '123'
        source_client = BridgeClient(source_mocked_client, self.topics, 2, self.topic_translator_config)
        target_mocked_client = Mock(spec=PahoMqttClient)
        target_mocked_client.id = '456'
        target_client = BridgeClient(target_mocked_client, self.topics, 2, self.topic_translator_config)
        source_client.bridge(target_client)
        target_client.bridge(source_client)
        msg = MQTTMessage(topic='test_topic'.encode('utf-8'))
        msg.payload = 'test_payload'
        msg.qos = 0
        msg.retain = True

        target_client.received(msg)
        time.sleep(2)
        source_client.received(msg)
        
        source_mocked_client.publish.assert_called_once()
        target_mocked_client.publish.assert_called_once()


if __name__ == '__main__':
    unittest.main()