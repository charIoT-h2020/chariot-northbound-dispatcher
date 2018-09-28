# -*- coding: utf-8 -*-
from chariot_northbound_dispatcher.model import Subscriber

rules = {
    'bms': {
        'subscribe': [
            'urn:ngsi-ld:5410ec4d1601_humidity',
            'urn:ngsi-ld:5410ec4d1601_temperature',
            'urn:ngsi-ld:5410ec4d1601_din01'
        ]
    },
    'security': {
        'subscribe': [
            'urn:ngsi-ld:5410ec4d1601_din02',
            'urn:ngsi-ld:5410ec4d1601_din03',
            'urn:ngsi-ld:5410ec4d1601_din04'
        ]
    }
}

class SubscriberResource(object):
    def __init__(self, engine):
        self.subscribers = [
            Subscriber('bms'),
            Subscriber('security')
        ]

    def on_post(self, req, resp):
        subscriber_id = req.get_json('id')
        sensor_id = req.get_json('sensor_id')

        resp.json = {
            'message': 'Ok'
        }
