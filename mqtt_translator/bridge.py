import logging
from .bridge_client import BridgeClient

class Bridge:

    def __init__(self, config):

        self.__source = BridgeClient(config['source'])
        self.__target = BridgeClient(config['target'])

        self.__source.bridge(self.__target)
        self.__target.bridge(self.__source)

        self.__source.connect()
        self.__target.connect()
        
        logging.info('Bridge created')

    def loop(self):

        self.__source.loop()
        self.__target.loop()