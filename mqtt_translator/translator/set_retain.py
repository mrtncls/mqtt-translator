import re
import copy
from .message_action import MessageAction


class SetRetain(MessageAction):

    @staticmethod
    def create(config):
        if 'set_retain' in config:
            return SetRetain(config['set_retain'])
        else:
            return None

    def perform(self, msg):
        for config in self._config:
            if self._isSettingNeeded(config, msg):
                self._setRetain(config, msg)

    def _isSettingNeeded(self, config, msg):
        if 'topic_fullmatch' in config:
            return None != re.fullmatch(config['topic_fullmatch'], msg.topic)
        return True

    def _setRetain(self, config, msg):
        msg.retain = config['retain']