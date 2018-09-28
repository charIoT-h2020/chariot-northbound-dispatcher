# -*- coding: utf-8 -*-


class Dispatcher(object):
    def __init__(self):
        pass

    def on_message(self, client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)
