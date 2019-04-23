# -*- coding: utf-8 -*-

import cgi
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
        logging.debug('Path: %s, Q: %s %s' % (path, q, req.headers['CONTENT-TYPE']))

        span = self.start_span('forward_message')
        url = self.services[engine]
        url = url % (path, q)
        span.set_tag('url', url)
        headers = self.inject_to_request_header(span, url)

        if req.content_type.find('multipart/form-data') > -1:
            try:
                logging.info('Forward multipart request')
                files = {}
                form_data = {}
                for key, value in req.params.items():
                    if isinstance(value, cgi.FieldStorage) :
                        files[value.name] = (value.filename, value.file, value.type)
                    else:
                        form_data[key] = value
                result = self.session.post(url, headers=headers, data=form_data, files=files)
            except Exception as ex:
                logging.error(ex)
        else:
            
            body = req.stream.read()
            if len(body) > 0:
                data = json.loads(body.decode('utf-8'))
            else:
                data = None

            if req.method == 'GET':
                result = self.session.get(url, headers=headers)
            elif req.method == 'POST':
                result = self.session.post(url, headers=headers, json=data)
            elif req.method == 'PUT':
                result = self.session.put(url, headers=headers, json=data)
            elif req.method == 'PATCH':
                result = self.session.patch(url, headers=headers, json=data)
            elif req.method == 'DELETE':
                result = self.session.delete(url, headers=headers)
            elif req.method == 'HEAD':
                result = self.session.head(url, headers=headers)
            elif req.method == 'OPTIONS':
                result = self.session.options(url, headers=headers)
            else:
                result = self.session.get(url, headers=headers)

        resp.status = str(result.status_code) + ' ' + result.reason
        resp.content_type = result.headers['content-type']
        resp.body = result.text
        self.close_span(span)

    def add_services(self, services):
        self.services = services