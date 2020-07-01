#!/usr/bin/python3

import sys

sys.path.append(".")
from broker import broker
import time

def on_message(client, userdata, message):
    msg_received = str(message.payload.decode("utf-8"))
    msg_topic    = message.topic
    msg_qos      = message.qos
    msg_retain   = message.retain
    print("message received ", msg_received)
    print("message topic=", msg_topic)
    print("message qos=", msg_qos)
    print("message retain flag=", msg_retain)
    return {"payload": msg_received, "topic": msg_topic, 
            "qos": msg_qos, "retain": msg_retain}

lil_client = broker(broker_adr="localhost", topic="leotest", client_name="letest")
lil_client.client_init()
lil_client.client.on_message = on_message
lil_client.client_connect()
lil_client.start_payload_loop()
lil_client.client_subscribe()

while True:
    lil_client.client_publish("saludos")
    # a = lil_client.client.on_message(lil_client.client)
    time.sleep(4)
    # print(msg_received)