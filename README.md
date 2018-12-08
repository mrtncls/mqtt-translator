# mqtt-translator

MQTT topic translator which can act as a MQTT bridge.

[![Build Status](https://travis-ci.com/mrtncls/mqtt-translator.svg?branch=master)](https://travis-ci.com/mrtncls/mqtt-translator)

## Launch

```
translate -c /config/configuration.yaml
```

## Docker image

https://hub.docker.com/r/mrtncls/mqtt-translator/

## Configuration

### Example: bridging with space replacement

```yaml
source:
  id: MQTT-Translator-Source
  host: source_mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
    - world/#
  publish:
    cooldown: 2
    translator:
      topic:
        - from: '_' 
          to: ' '
target:
  id: MQTT-Translator-Target
  host: target_mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
    - world/#
  publish:
    cooldown: 2
    translator:
      topic:
        - from: ' ' 
          to: '_'
```

### Example: topic translate

```yaml
source:
  id: MQTT-Translator-Source
  host: mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
    - 1235332/#
  publish:
    cooldown: 2
target:
  id: MQTT-Translator-Target
  host: mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
  publish:
    cooldown: 2
    translator:
      topic:
        - from: '1235332' 
          to: 'temp_sensor'
```
