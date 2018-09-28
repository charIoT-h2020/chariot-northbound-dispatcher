# -*- coding: utf-8 -*-


class Subscriber(object):
    def __init__(self, subscriber_id):
        self.id = subscriber_id
        self.sensors = set()

    def dict(self):
        return {
            'id': self.id,
            'sensors': list(self.sensors)
        }
