# -*- coding: utf-8 -*-

import falcon
import falcon_jsonify

from chariot_base.connector import LocalConnector

from chariot_northbound_dispatcher.dispatcher import Dispatcher
from chariot_northbound_dispatcher.resources import SubscriberResource


# Initialize connection to northbound
northbound = LocalConnector('northbound', '172.18.1.3')
northbound.start(False)

engine = Dispatcher()

northbound.on_log = engine.on_log
northbound.on_message = engine.on_message

app = falcon.API(middleware=[
    falcon_jsonify.Middleware(help_messages=True)
])

message = SubscriberResource(engine)

app.add_route('/subscriber', message)
