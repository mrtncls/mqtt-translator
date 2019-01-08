# MQTT Translator

[![Build Status](https://travis-ci.com/mrtncls/mqtt-translator.svg?branch=master)](https://travis-ci.com/mrtncls/mqtt-translator)
[![codecov](https://codecov.io/gh/mrtncls/mqtt-translator/branch/master/graph/badge.svg)](https://codecov.io/gh/mrtncls/mqtt-translator)
[![Docker image version](https://images.microbadger.com/badges/version/mrtncls/mqtt-translator.svg)](https://hub.docker.com/r/mrtncls/mqtt-translator)
[![Docker image](https://images.microbadger.com/badges/image/mrtncls/mqtt-translator.svg)](https://hub.docker.com/r/mrtncls/mqtt-translator)

MQTT topic translator which can act as a MQTT bridge.

## Launch

Download all files and execute:

```
python -m mqtt_translator -c /config/configuration.yaml
```

or use the docker image on https://hub.docker.com/r/mrtncls/mqtt-translator

## Configuration

Available translator modules:

- Topic replace
- Payload replace
- Topic & payload substitute

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
      - topic_replace:
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
      - topic_replace:
        - from: ' ' 
          to: '_'
```

### Example: topic replace

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
    translator:
target:
  id: MQTT-Translator-Target
  host: mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
  publish:
    cooldown: 2
    translator:
      - topic_replace:
        - from: '1235332' 
          to: 'temp_sensor'
```

### Example: topic & payload substitution

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
    translator:
target:
  id: MQTT-Translator-Target
  host: mqttbroker
  port: 1883
  keepalive_interval: 60
  topics:
  publish:
    cooldown: 2
    translator:
      - topic_replace:
        - from: ' ' 
          to: '_'
        - from: '1235332' 
          to: 'temp_sensor'
      - topic_payload_subst:
        - from_topic: 'home',
          from_payload: '50',
          to_topic: 'state',
          to_payload: '50 degrees'
```
