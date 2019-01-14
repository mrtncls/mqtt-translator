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

or use the docker image: https://hub.docker.com/r/mrtncls/mqtt-translator

## Configuration

Available translator modules:

### Topic

Replaces a part (from) of the MQTT topic with another part (to).

*Example config:*

```yaml
topic:
  - from: lookup
    to: replace
  - from: lookup2
    to: replace2
```

### Payload

Replaces a part (from) of a stringtype payload with another part (to).

*Example config:*

```yaml
payload:
  - from: old_value
    to: new_value
  - from: old_value2
    to: new_value2
```

### Regular expression

Matches MQTT message by *topic_search* and *payload_search* expressions (https://docs.python.org/3/library/re.html). Renders *topic_template* and *payload_template* by using the found regexp groups.

With *[topic.1]* and *[topic.99]* in your template, the first and 99th group from the *topic_search* expression will be substituted. This works the same for payload with *[payload.x]*.

A template will substitute only the found part. So, remaining pre- and/or suffixes will stay.

In case no search was done (topic_search or payload_search missing) but a template is supplied, it will replace the whole topic or payload.

*Example config:*

```yaml
regexp:
  - topic_search: temp/(auto)
    payload_search: (heat) (\d+)
    topic_template: temp/[payload.1]
    payload_template: [payload.2] - [topic.1]
  - ...
```

*Example with result:*

```yaml
regexp:
  - payload_search: (\w+)|(\d+)|(\w+)
    topic_template: house/[payload.1]/temperature
    payload_template: [payload.2] [payload.3]
  - ...
```
| | Topic | Payload |
| --- | --- | --- |
| Original | house/87946548/auto | bedroom,24,auto |
| Translated | house/bedroom/temperature | 24 auto |

## Examples

### Bridging with space replacement

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
      - topic:
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
      - topic:
        - from: ' ' 
          to: '_'
```

### Topic replace

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
      - topic:
        - from: '1235332' 
          to: 'temp_sensor'
```