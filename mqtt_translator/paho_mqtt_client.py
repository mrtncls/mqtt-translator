import logging
from paho.mqtt.client import Client, MQTTv311, MQTT_ERR_SUCCESS


class PahoMqttClient(Client):

    def __init__(self, id, host, port, keepalive_interval):

        super().__init__(client_id=id, clean_session=True,
                         userdata=None, protocol=MQTTv311, transport='tcp')

        self.id = id
        self.connect_async(host, port, keepalive_interval)

    def loop(self):

        loopResult = super().loop(0.01, 1)

        if loopResult != MQTT_ERR_SUCCESS:
            self._reconnect_wait()
            try:
                logging.info('%s connecting...', self._client_id)
                self.reconnect()
            except Exception as e:
                logging.error('%s connect failed: %s', self._client_id, e)
