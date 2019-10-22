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

        span = self.start_span('forward_message')
        url = self.get_service_url(span, req, resp, engine, path)
        span.set_tag('url', url)

        headers = self.inject_to_request_header(span, url)

        if req.content_type is not None and req.content_type.find('multipart/form-data') > -1:
            result = self.forward_file(req, resp)
        else:
            data = self.get_body(req, resp)
            result = self.forward(req, resp, url, headers, data)

        resp.status = str(result.status_code) + ' ' + result.reason

        resp.content_type = result.headers['content-type']
        resp.body = result.text
        self.close_span(span)

    def forward_file(self, req, resp):
        try:
            logging.info('Forward multipart request')
            files = {}
            form_data = {}
            for key, value in req.params.items():
                if isinstance(value, cgi.FieldStorage) :
                    files[value.name] = (value.filename, value.file, value.type)
                else:
                    form_data[key] = value
            return self.session.post(url, headers=headers, data=form_data, files=files)
        except Exception as ex:
            logging.error(ex)

    def get_body(self, req, resp):
        body = req.stream.read()
        if len(body) > 0:
            data = json.loads(body.decode('utf-8'))
            logging.debug(f'Serialized data: {data}')
        else:
            data = None
        return data

    def forward(self, req, resp, url, headers, data=None):
        if req.method == 'GET':
            result = self.session.get(url, headers=headers)
        elif req.method == 'POST':
            result = self.session.post(url, headers=headers, json=data)
        elif req.method == 'PUT':
            result = self.session.put(url, headers=headers, json=data)
        elif req.method == 'PATCH':
            result = self.session.patch(url, headers=headers, json=data)
        elif req.method == 'DELETE':
            result = self.session.delete(url, headers=headers, json=data)
        elif req.method == 'HEAD':
            result = self.session.head(url, headers=headers)
        elif req.method == 'OPTIONS':
            result = self.session.options(url, headers=headers)
        else:
            result = self.session.get(url, headers=headers)

        return result

    def get_service_url(self, span, req, resp, engine, path=None):
        path = path or ''
        q = req.query_string or ''
        url = self.services[engine]
        url = url % (path, q)
        span.set_tag('url', url)
        logging.debug(f'Url: {url}, Path: {path}, Q: {q}')

        if not q:
            url = url.replace('?', '')

        if not path:
            url = url.strip("/")

        return url

    def add_services(self, services):
        self.services = services
