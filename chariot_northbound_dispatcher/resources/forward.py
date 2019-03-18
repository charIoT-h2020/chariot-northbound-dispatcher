# -*- coding: utf-8 -*-

import json
import falcon
import logging
import requests

from opentracing.ext import tags
from opentracing.propagation import Format

from chariot_base.utilities import Traceable


class SinkAdapter(Traceable):

    def __init__(self):
        super(Traceable, self).__init__()
        self.services = None
        self.session = requests.Session()
        self.session.trust_env = False

    def __call__(self, req, resp, engine, path=None):
        path = path or ''
        q = req.query_string or ''
        logging.debug('Path: %s, Q: %s' % (path, q))
        span = self.start_span('forward_message')
        url = self.services[engine]
        url = url % (path, q)
        span.set_tag('url', url)
        headers = self.inject_to_request_header(span, url)
        result = self.session.get(url, headers=headers)
        resp.status = str(result.status_code) + ' ' + result.reason
        resp.content_type = result.headers['content-type']
        resp.body = result.text
        self.close_span(span)

    def add_services(self, services):
        self.services = services