FROM registry.gitlab.com/chariot-h2020/chariot_base:latest

WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install falcon-jsonify && python setup.py install

EXPOSE 5080

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/usr/src/app/gunicorn.py", "chariot_northbound_dispatcher.app:app"]