# -*- coding: utf-8 -*-
import json

from chariot_base.utilities import Traceable
from chariot_base.model import Subscriber


class Dispatcher(Traceable):
    def __init__(self):
        self.tracer = None
        self.southbound = None
        self.northbound = None

        self.subscribers = {
            'bms': Subscriber('bms'),
            'security': Subscriber('security')
        }

        self.subscribers['bms'].sensors = {
            '5410ec4d1601_humidity',
            '5410ec4d1601_temperature',
            '5410ec4d1601_din01'
        }

        self.subscribers['security'].sensors = {
            '5410ec4d1601_din02',
            '5410ec4d1601_din03',
            '5410ec4d1601_din04'
        }

    def inject(self, southbound, northbound):
        self.southbound = southbound
        self.northbound = northbound

    def subscribe_to_southbound(self):
        self.southbound.subscribe('northbound/#', qos=0)

    def forward(self, message):
        destination = message['destination']
        sensor_id = message['sensor_id']
        value = json.dumps(message['value'])
        print(destination, sensor_id, value)
        if self.subscribers[destination] is not None:
            if sensor_id in self.subscribers[destination].sensors:
                self.northbound.publish('%s/%s' % (destination, sensor_id), value)
