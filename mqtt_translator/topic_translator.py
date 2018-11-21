class TopicTranslator:
    
    def __init__(self, config):
        self.__config = config

    def translate(self, topic):
        result = topic
        for topic_replace in self.__config:
            result = result.replace(topic_replace['from'], topic_replace['to'])
        return result