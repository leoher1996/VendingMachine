#!/usr/bin/python3

import sys

sys.path.append(".")
from broker import broker
import time

# Triggers when a message is received from the MQTT subscribed channel.
def on_message(client, userdata, message):
    msg_received = str(message.payload.decode("utf-8"))
    msg_topic    = message.topic
    msg_qos      = message.qos
    msg_retain   = message.retain
    print("message received ", msg_received)
    print("message topic=", msg_topic)
    print("message qos=", msg_qos)
    print("message retain flag=", msg_retain)
    
    # Writes received messages to a log file with a timestamp.
    f = open("vending_machine.log", "a")
    f.write(f"{msg_received} :: {time.ctime(time.time())}\n")
    f.close()

lil_client = broker(broker_adr="64.227.111.82", topic="general/vending_lw", client_name="server", port=1884)
lil_client.client_init()
lil_client.client.on_message = on_message
lil_client.client_connect()
lil_client.start_payload_loop()
lil_client.client_subscribe()

while True:
    time.sleep(1)