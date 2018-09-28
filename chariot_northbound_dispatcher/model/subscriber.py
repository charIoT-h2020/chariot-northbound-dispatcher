# -*- coding: utf-8 -*-


class Subscriber(object):
    def __init__(self, subscriber_id):
        self.id = subscriber_id
        self.sensors = []
