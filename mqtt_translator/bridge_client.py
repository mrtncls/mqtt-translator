import logging
import time
from paho.mqtt.client import Client, MQTTv311, MQTT_ERR_SUCCESS
from .message_history import MessageHistory
from .topic_translator import TopicTranslator

def connected(client, userdata, flags, rc):
    
    logging.info('%s connected', client._client_id)

    for topic in client.config['topics']:
        try:
            client.subscribe(topic)
            logging.debug('%s subscribed to %s', client._client_id, topic)
        except Exception as e:
            logging.error('%s subscribe failed: %s', client._client_id, e)

def disconnected(client, userdata, rc):
    
    logging.info('%s disconnected with status %s', client._client_id, rc)

    if (rc != MQTT_ERR_SUCCESS):
        client._reconnect()

def received(client, userdata, msg):
    
    hash = msg.topic+str(msg.payload)

    if not client.publishMsgHistory.has_message(hash):
        logging.debug("client=%s  topic=\"%s\" payload=\"%s\"", client._client_id, msg.topic, msg.payload)
        try:
            client.other_client.publish(msg.topic, msg.payload, msg.qos, msg.retain)
        except Exception as e:
            logging.error('Publish failed: %s', e)

class BridgeClient(Client):

    def __init__(self, config, clean_session=True, userdata=None, protocol=MQTTv311, transport='tcp'):

        super().__init__(client_id=config['id'], clean_session=clean_session, userdata=userdata, protocol=protocol, transport=transport)

        self.config = config

        publish_config = config['publish']
        self.publishMsgHistory = MessageHistory(publish_config['cooldown'])
        self.__translator = TopicTranslator(publish_config['translator']['topic'])        

        self.on_connect = connected
        self.on_disconnect = disconnected
        self.on_message = received

        self.__reconnecting = False

    def bridge(self, other_client):

        self.other_client = other_client

    def connect(self):
        
        try:
            super().connect(self.config['host'], self.config['port'], self.config['keepalive_interval'])
        except:
            self._reconnect()

    def _reconnect(self):

        if self.__reconnecting:
            return

        self.__reconnecting = True
        while self.__reconnecting:

            try:
                logging.info('%s connecting...', self._client_id)        
                self.reconnect()
                self.__reconnecting = False
            except Exception as e:
                logging.error('%s connect failed: %s', self._client_id, e)
                time.sleep(1)

    def loop(self, timeout=0.01, max_packets=1):

        self.publishMsgHistory.purge()
        return super().loop(timeout, max_packets)

    def publish(self, topic, payload=None, qos=0, retain=False):

        translated_topic = self.__translator.translate(topic)
        logging.debug("client=%s  topic=\"%s\" payload=\"%s\"", self._client_id, translated_topic, payload)

        hash = translated_topic+str(payload)
        self.publishMsgHistory.add_message(hash)
        
        return super().publish(translated_topic, payload=payload, qos=qos, retain=retain)