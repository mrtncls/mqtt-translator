from setuptools import setup

setup(
   name='mqtt-translationbridge',
   version='0.1',
   description='MQTT bridge with support for message translation',
   author='Maarten Claes',
   author_email='mrtncls@gmail.com',
   packages=['mqtt-translationbridge'],
   install_requires=['PyYAML', 'paho-mqtt'],
)