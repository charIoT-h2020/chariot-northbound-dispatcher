# -*- coding: utf-8 -*-
import json

import falcon
import falcon_jsonify

from chariot_base.connector import LocalConnector

from chariot_northbound_dispatcher.dispatcher import Dispatcher
from chariot_northbound_dispatcher.resources import SubscriberResource


class NorthboundConnector(LocalConnector):
    def on_log(self, client, userdata, level, buf):
        print("log[%s]: %s" % (level, buf))


class SouthboundConnector(LocalConnector):
    def __init__(self, client_od, broker, controller):
        super().__init__(client_od, broker)
        self.dispatcher = controller

    def on_log(self, client, userdata, level, buf):
        print("log[%s]: %s" % (level, buf))

    def on_message(self, client, userdata, message):
        self.dispatcher.forward(json.loads(str(message.payload.decode("utf-8"))))


dispatcher = Dispatcher()

northbound = NorthboundConnector('northbound', '172.18.1.3')
southbound = SouthboundConnector('southbound', '172.18.1.2', dispatcher)

dispatcher.inject(southbound, northbound)
dispatcher.start()

app = falcon.API(middleware=[
    falcon_jsonify.Middleware(help_messages=True)
])

messageResource = SubscriberResource(dispatcher)

app.add_route('/subscriber', messageResource)
