# -*- coding: utf-8 -*-
import json

from chariot_base.model import Subscriber


class Dispatcher(object):
    def __init__(self):
        self.subscribers = {
            'urn:ngsi-ld:bms': Subscriber('urn:ngsi-ld:bms'),
            'urn:ngsi-ld:security': Subscriber('urn:ngsi-ld:security')
        }

        self.subscribers['urn:ngsi-ld:bms'].sensors = {
            'urn:ngsi-ld:5410ec4d1601_humidity',
            'urn:ngsi-ld:5410ec4d1601_temperature',
            'urn:ngsi-ld:5410ec4d1601_din01'
        }

        self.subscribers['urn:ngsi-ld:security'].sensors = {
            'urn:ngsi-ld:5410ec4d1601_din02',
            'urn:ngsi-ld:5410ec4d1601_din03',
            'urn:ngsi-ld:5410ec4d1601_din04'
        }

        self.southbound = None
        self.northbound = None

    def inject(self, southbound, northbound):
        self.southbound = southbound
        self.northbound = northbound

    def start(self):
        self.northbound.start(False)
        self.southbound.start(False)
        self.southbound.subscribe([
            ('northbound/#', 0)
        ])

    def forward(self, message):
        destination = message['destination']
        sensor_id = message['sensor_id']
        value = json.dumps(message['value'])

        if sensor_id in self.southbound[destination]:
            self.northbound.publish('%s/%s' % (destination, sensor_id), value)
