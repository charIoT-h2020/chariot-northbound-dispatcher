# -*- coding: utf-8 -*-

import os
import uuid
import json
import gmqtt
import asyncio
import signal
import logging
import falcon

from wsgiref import simple_server
from falcon_multipart.middleware import MultipartMiddleware

from chariot_base.utilities import Tracer
from chariot_base.utilities import open_config_file

from chariot_northbound_dispatcher import __service_name__
from chariot_northbound_dispatcher.resources.forward import SinkAdapter

opts = open_config_file()

options_engine = opts.northbound_dispatcher
options_tracer = opts.tracer

app = falcon.API(middleware=[
    MultipartMiddleware(),
])

sink = SinkAdapter()

sink.add_services(options_engine['services'])

if options_tracer['enabled']:
    options_tracer['service'] = __service_name__
    logging.debug(f'Enabling tracing for service "{__service_name__}"')

    tracer = Tracer(options_tracer)
    tracer.init_tracer()
    sink.inject_tracer(tracer)

app.add_sink(sink, r'/(?P<engine>[a-zA-Z]+)(/(?P<path>.*))?\Z')


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()