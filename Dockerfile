FROM python:3.6-alpine

WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN python setup.py install

EXPOSE 8020

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/usr/src/app/gunicorn.py", "chariot_northbound_dispatcher.app:app"]
