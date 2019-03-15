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
from wsgiref import simple_server

from chariot_northbound_dispatcher.resources.forward import SinkAdapter
from chariot_base.utilities import Tracer


from chariot_base.utilities import open_config_file

opts = open_config_file()

options_engine = opts.northbound_dispatcher
options_tracer = opts.tracer

tracer = Tracer(options_tracer)
tracer.init_tracer()

app = falcon.API()

sink = SinkAdapter()
sink.inject_tracer(tracer)

app.add_sink(sink, r'/(?P<engine>[a-zA-Z]+)(/(?P<path>.*))?\Z')


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()