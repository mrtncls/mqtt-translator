import logging
from .paho_mqtt_client import PahoMqttClient
from .bridge_client import BridgeClient


class Bridge:

    def __init__(self, config):

        sourceConfig = config['source']
        sourcePublishConfig = sourceConfig['publish']
        sourceClient = PahoMqttClient(
            sourceConfig['id'], sourceConfig['host'], sourceConfig['port'], sourceConfig['keepalive_interval'])
        self._source = BridgeClient(
            sourceClient, sourceConfig['topics'], sourcePublishConfig['cooldown'], sourcePublishConfig['translator'])

        targetConfig = config['target']
        targetPublishConfig = targetConfig['publish']
        targetClient = PahoMqttClient(
            targetConfig['id'], targetConfig['host'], targetConfig['port'], targetConfig['keepalive_interval'])
        self._target = BridgeClient(
            targetClient, targetConfig['topics'], targetPublishConfig['cooldown'], targetPublishConfig['translator'])

        self._source.bridge(self._target)
        self._target.bridge(self._source)

        logging.info('Bridge created')

    def loop(self):

        self._source.loop()
        self._target.loop()
