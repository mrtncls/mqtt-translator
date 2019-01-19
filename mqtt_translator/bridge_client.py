import logging
from .paho_mqtt_client import PahoMqttClient
from .message_history import MessageHistory
from .translator.message_translator import MessageTranslator


class BridgeClient():

    def __init__(self, client, topics, cooldown, translator_config):

        self.client = client
        self.id = client.id
        self.topics = topics
        self._publishMsgHistory = MessageHistory(cooldown)
        self._translator = MessageTranslator(translator_config)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):

        logging.info(f'{self.id} connected')

        for topic in self.topics:
            try:
                self.client.subscribe(topic)
                logging.debug(f'{self.id} subscribed to {topic}')
            except Exception as e:
                logging.error(f'{self.id} subscribe failed: {e}')

    def on_message(self, client, userdata, msg):

        logging.debug(
            f'{self.id} received topic={msg.topic} payload={msg.payload} qos={msg.qos} retain={msg.retain}')

        hash = self._getMessageHash(msg)

        if self._isNotSentInCooldownPeriod(hash):
            self._translator.translate(msg)
            self._publish_on_other_client(msg)

    def bridge(self, other):

        self._other_bridge_client = other

    def loop(self):

        self._publishMsgHistory.purge()
        self.client.loop()

    def _getMessageHash(self, msg):

        return msg.topic+str(msg.payload)

    def _isNotSentInCooldownPeriod(self, hash):

        return not self._publishMsgHistory.has_message(hash)

    def _publish_on_other_client(self, msg):

        try:
            self._other_bridge_client._publish(msg)
        except Exception as e:
            logging.error(f'{self.id} publish failed: {e}')

    def _publish(self, msg):

        logging.debug(
            f'{self.id} published topic={msg.topic} payload={msg.payload} qos={msg.qos} retain={msg.retain}')

        hash = msg.topic+str(msg.payload)
        self._publishMsgHistory.add_message(hash)

        return self.client.publish(msg.topic, payload=msg.payload, qos=msg.qos, retain=msg.retain)
