# -*- coding: utf-8 -*-

import os
import uuid
import json
import gmqtt
import asyncio
import signal
import logging
import falcon
import falcon_jsonify
import time

from chariot_base.connector import LocalConnector

from chariot_northbound_dispatcher.dispatcher import Dispatcher
from chariot_northbound_dispatcher.resources import SubscriberResource

from chariot_base.utilities import open_config_file, Tracer

from chariot_base.connector import LocalConnector, create_client


class SouthboundConnector(LocalConnector):
    def __init__(self, options):
        super(SouthboundConnector, self).__init__()
        self.dispatcher = None

    def on_message(self, client, topic, payload, qos, properties):
        msg = payload.decode('utf-8')
        deserialized_model = json.loads(msg)
        span = self.start_span_from_message('on_message', deserialized_model)
        try:
            self.dispatcher.forward(deserialized_model, span)
            self.close_span(span)
        except Exception as ex:
            self.error(span, ex)
            logging.error(ex)

    def inject_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher

class NorthboundConnector(LocalConnector):
    def __init__(self, options):
        super(NorthboundConnector, self).__init__()


STOP = asyncio.Event()


def ask_exit(*args):
    logging.info('Stoping....')
    STOP.set()


async def main(args=None):

    opts = open_config_file()

    options_engine = opts.northbound_dispatcher
    options_tracer = opts.tracer

    tracer = Tracer(options_tracer)
    tracer.init_tracer()

    logging.debug("host: {host}:{port}, enabled: {enabled}, service: {service}".format(**options_tracer))

    southbound = SouthboundConnector(options_engine)
    southbound.inject_tracer(tracer)
    client_south = await create_client(opts.brokers.southbound)
    southbound.register_for_client(client_south)

    northbound = NorthboundConnector(options_engine)
    northbound.inject_tracer(tracer)
    client_north = await create_client(opts.brokers.northbound)
    northbound.register_for_client(client_north)

    dispatcher = Dispatcher(options_engine)
    southbound.inject_dispatcher(dispatcher)
    dispatcher.inject(southbound, northbound)
    dispatcher.inject_tracer(tracer)
    dispatcher.subscribe_to_southbound()

    logging.info('Waiting message from Privacy Engine')
    await STOP.wait()
    await client_south.disconnect()
    await client_north.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main())
    logging.info('Stopped....')