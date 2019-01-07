import logging
from .paho_mqtt_client import PahoMqttClient
from .message_history import MessageHistory
from .translator.message_translator import MessageTranslator


def connected(client, userdata, flags, rc):
    userdata.connected()


def received(client, userdata, msg):
    userdata.received(msg)


class BridgeClient():

    def __init__(self, client, topics, cooldown, translator_config):

        self.client = client
        self.id = client.id
        self.topics = topics
        self._publishMsgHistory = MessageHistory(cooldown)
        self._translator = MessageTranslator(translator_config)

        self.client.user_data_set(self)

        self.client.on_connect = connected
        self.client.on_message = received

    def bridge(self, other):

        self._other_bridge_client = other

    def loop(self):

        self._publishMsgHistory.purge()
        self.client.loop()

    def connected(self):

        logging.info('%s connected', self.id)

        for topic in self.topics:
            try:
                self.client.subscribe(topic)
                logging.debug('%s subscribed to %s', self.id, topic)
            except Exception as e:
                logging.error('%s subscribe failed: %s', self.id, e)

    def received(self, msg):

        logging.debug("%s received topic=\"%s\" payload=\"%s\"",
                      self.id, msg.topic, msg.payload)

        hash = self._getMessageHash(msg)

        if self._isNotSentInCooldownPeriod(hash):
            translated_msg = self._translator.translate(msg)
            self._publish_on_other_client(translated_msg)

    def _getMessageHash(self, msg):

        return msg.topic+str(msg.payload)

    def _isNotSentInCooldownPeriod(self, hash):

        return not self._publishMsgHistory.has_message(hash)

    def _publish_on_other_client(self, msg):

        try:
            self._other_bridge_client._publish(msg)
        except Exception as e:
            logging.error('%s publish failed: %s', self.id, e)

    def _publish(self, msg):

        logging.debug("%s published topic=\"%s\" payload=\"%s\"",
                      self.id, msg.topic, msg.payload)

        hash = msg.topic+str(msg.payload)
        self._publishMsgHistory.add_message(hash)

        return self.client.publish(msg.topic, payload=msg.payload, qos=msg.qos, retain=msg.retain)
