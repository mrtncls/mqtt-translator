import logging
import yaml
import argparse
from mqtt_translator.bridge import Bridge


def main():

    parser = argparse.ArgumentParser(prog='mqtt-translator',
        description='MQTT topic translator which can act as a MQTT bridge.')
    parser.add_argument('-c', '--config-file', required=True,
                        help='Configuration YAML file')
    parser.add_argument('-v ', '--version',
                        action='version', version='%(prog)s 0.1')
    parser.add_argument('-d ', '--debug', action="count", default=1,
                        help='Increase log level, add more -d to increase verbosity')

    args = parser.parse_args()

    if args.debug >= 2:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(funcName)s: %(message)s', level=logging.DEBUG)
    elif args.debug >= 1:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(funcName)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(funcName)s: %(message)s', level=logging.WARN)
    logging.info('Loading setup...')

    with open(args.config_file, 'r') as stream:
        config = yaml.load(stream)

    bridge = Bridge(config)

    logging.info('Setup completed')

    while True:
        bridge.loop()


if __name__ == "__main__":
    main()
