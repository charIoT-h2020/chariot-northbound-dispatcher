# -*- coding: utf-8 -*-
from chariot_northbound_dispatcher.model import Subscriber


class SubscriberResource(object):
    def __init__(self, engine):
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

    def on_post(self, req, resp):
        subscriber_id = req.get_json('id')
        sensor_id = req.get_json('sensor_id')

        rule = self.subscribers[subscriber_id]
        rule.sensors.add(sensor_id)

        resp.json = rule.dict()