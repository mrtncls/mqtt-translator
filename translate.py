import logging
import yaml
import argparse
from mqtt_translator.bridge import Bridge


def main():

    parser = argparse.ArgumentParser(description='MQTT topic translator which can act as a MQTT bridge.')
    parser.add_argument('-c', '--config-file', required=True, help='Configuration YAML file')
    parser.add_argument('-v ', '--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s: %(message)s', level=logging.DEBUG)
    logging.info('Loading setup...')

    with open(args.config_file, 'r') as stream:
        config = yaml.load(stream)

    bridge = Bridge(config)

    logging.info('Setup completed')

    while True:
        bridge.loop()


if __name__ == "__main__":
    main()