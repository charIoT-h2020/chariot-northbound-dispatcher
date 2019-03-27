# -*- coding: utf-8 -*-
import json
import logging

from chariot_base.utilities import Traceable
from chariot_base.model import Subscriber


class Dispatcher(Traceable):
    def __init__(self):
        self.tracer = None
        self.southbound = None
        self.northbound = None

        self.subscribers = {
            'BMS': Subscriber('BMS')
        }

        self.subscribers['BMS'].sensors = {
            'device_52806c75c3fd_Sensor04'
        }

    def inject(self, southbound, northbound):
        self.southbound = southbound
        self.northbound = northbound

    def subscribe_to_southbound(self):
        self.southbound.subscribe('northbound/#', qos=0)

    def forward(self, message, span):
        try:
            destination = message['destination']
            sensor_id = message['sensor_id']
            value = json.dumps(message['value'])

            logging.debug('Message %s from %s send to %s' % (value, sensor_id, destination))
            self.set_tag(span, 'destination', destination)

            if self.subscribers[destination] is not None:
                if sensor_id in self.subscribers[destination].sensors:
                    self.northbound.publish('%s/%s' % (destination, sensor_id), value)

        except:
            raise