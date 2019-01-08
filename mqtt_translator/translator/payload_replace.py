from .message_translator_base import MessageTranslatorBase


class PayloadReplace(MessageTranslatorBase):

    @staticmethod
    def create(config):
        if 'payload_replace' in config:
            return PayloadReplace(config['payload_replace'])
        else:
            return None

    def translate(self, msg):
        payload = msg.payload.decode('utf-8')
        for payload_replace in self._config:
            payload = payload.replace(payload_replace['from'], payload_replace['to'])

        msg.payload = payload.encode('utf-8')

