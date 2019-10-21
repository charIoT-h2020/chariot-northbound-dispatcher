# -*- coding: utf-8 -*-
import json
import logging
import requests

from chariot_base.utilities import Traceable
from chariot_base.model import Subscriber


class Dispatcher(Traceable):
    def __init__(self, options):
        self.tracer = None
        self.southbound = None
        self.northbound = None

        self.session = requests.Session()
        self.session.trust_env = False
        self.options = options

        if 'subscriber_url' not in self.options:
            raise Exception('subscriber_url is missing')

    def inject(self, southbound, northbound):
        self.southbound = southbound
        self.northbound = northbound

    def subscribe_to_southbound(self):
        self.southbound.subscribe('northbound/#', qos=0)

    def forward(self, message, span):
        try:
            destination = message['destination']
            sensor_id = message['sensor_id'].lower()
            original_message = json.loads(message['value'])
            message['value'] = original_message
            value = message

            logging.debug('Message %s from %s send to %s' % (value, sensor_id, destination))
            self.set_tag(span, 'destination', destination)

            url = self.options['subscriber_url'].format(**{'destination': destination})
            headers = self.inject_to_request_header(span, url)
            self.set_tag(span, 'url', url)
            logging.debug('Retrieving subscription for: %s/%s' % (url, headers))
            result = self.session.get(url, headers=headers)

            if result is not None:
                info = result.json()
                logging.debug('Retrieve subscription %s info: %s' % (sensor_id, info))

                if sensor_id in info['sensors']:
                    topic = '%s/%s' % (destination, sensor_id)
                    logging.debug('Retrieve subscription info: %s' % (topic))
                    self.northbound.publish(topic, value)

        except:
            raise
