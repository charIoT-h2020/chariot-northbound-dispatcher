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
        self.engines = {
            'alerts': 'http://localhost:9000/alerts/%s'
        }
        self.session = requests.Session()
        self.session.trust_env = False

    def __call__(self, req, resp, engine, path=None):
        path = path or ''

        span = self.start_span('forward_message')
        url = self.engines[engine]
        url = url % path
        span.set_tag('url', url)

        span.set_tag(tags.HTTP_METHOD, 'GET')
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        self.tracer.tracer.inject(span, Format.HTTP_HEADERS, headers)

        result = self.session.get(url, headers=headers)

        resp.status = str(result.status_code) + ' ' + result.reason
        resp.content_type = result.headers['content-type']
        resp.body = result.text
        span.finish()
