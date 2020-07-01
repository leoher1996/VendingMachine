#!/usr/bin/python3

# System imports.
import paho.mqtt.client as mqtt
import time

class broker:
    
   def __init__(self, broker_adr, topic, client_name, port=1883, keepalive=60):
      self.broker_adr  = broker_adr    # Use localhost for local testing purposes.
      self.topic       = topic         # Server topic to subscribe and publish to.
      self.client_name = client_name   # Make sure this value is unique for every instance.
      self.port        = port          # Default is 1883.
      self.keepalive   = keepalive     # Recommended value is 60.
      self.client      = 0
   
   # Initializes an instance of mqtt client to communicate with the server.
   def client_init(self):
      self.client = mqtt.Client(self.client_name)
      
      return 0
   
   # Connects to the defined server host.
   def client_connect(self):
      try:
         self.client.connect(host=self.broker_adr, port=self.port, keepalive=self.keepalive)
         
         # Attach on_message function to callback
         # self.client.on_message = on_message
         
         return 0
      
      except AttributeError:
         print("-E- You have not initialized a connection with the server host.")
      
         return 1
   
   # Terminates connection with server host.
   def client_disconnect(self):
      self.client.disconnect()
      
      return 0
   
   # Subscribe to a specific topic from the server host.
   def client_subscribe(self):
      self.client.subscribe(topic=self.topic)
      
      return 0
   
   # Sends payload message to specified topic.
   def client_publish(self, payload):
      self.client.publish(topic=self.topic, payload=payload)
      time.sleep(4)
      
      return 0
  
   # This function is executed on the main server to wait for new payload messages
   # from the different vending machines.
   def start_payload_loop(self):
      self.client.loop_start()
      
      return 0
   
   # Stops the client callback loop.
   def stop_payload_loop(self):
      time.sleep(4) #gives some time to process any remaining payloads.
      self.client.loop_stop()
      
      return 0
         
   
if __name__ == '__main__':
   pass
