# -*- coding: utf-8 -*-


class SubscriberResource(object):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def on_post(self, req, resp):
        subscriber_id = req.get_json('id')
        sensor_id = req.get_json('sensor_id')

        rule = self.dispatcher.subscribers[subscriber_id]
        rule.sensors.add(sensor_id)

        resp.json = rule.dict()
