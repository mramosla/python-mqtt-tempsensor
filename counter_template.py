import time
from time import sleep
import datetime
from datetime import datetime
import json
import requests


import paho.mqtt.client as mqtt
import mqtt_init

import twilio_text
import ssl

import socket

# URL To send shutdown command
URL = mqtt_init.url

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

# Globals
lastTemp = 0

status_code = 0
counter = 0
# Set wait period/keepalive
timeout = mqtt_init.timeout
timeout_default = mqtt_init.timeout_default

temp_stats = {
  "tempc": 0,
  "tempf": 0,
  "humidity": 0,
  "temp_status": "Normal",
  "timestamp": ""
}

texts = {
  "Warning": "Alert: office temp in Warning zone",
  "Danger": "Alert: office temp in Danger zone. Shutdown initiated",
  "shutdown": "Office temp in danger zone. Server shutdown sent.",
  "error": "Alert: Server not responding. Shutdown failed."
}

##### Begin MQTT Settings #####

# Define callbacks
# def on_log(client, userdata, level, buf):
#   print("log: "+buf)

def on_log(client, userdata, level, buf):
  
  #print("log: "+buf)

  timestamp = datetime.now()
  
  # Filter out unwanted keepalive logs
  if buf != "Sending PINGREQ":
    if buf != "Received PINGRESP":
      # Print logs to console
      if level == 1:
        print('INFO: {}'.format(buf))
        print('Timestamp: {}\n'.format(timestamp))
      if level == 2:
        print('NOTICE: {}'.format(buf))
        print('Timestamp: {}\n'.format(timestamp))
      if level == 4:
        print('WARNING: {}'.format(buf))
        print('Timestamp: {}\n'.format(timestamp))
      if level == 8:
        print('ERROR: {}'.format(buf))
        print('Timestamp: {}\n'.format(timestamp))
      if level == 16:
        print('DEBUG: {}'.format(buf))
        print('Timestamp: {}\n'.format(timestamp))

def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("connected OK")
  else:
    print("Bad Connection Returned code=", rc)

def on_disconnect(client, userdata, rc):
  if rc !=0: 
   print("Disconnect: ", rc)

def on_message(client, userdata, msg):
  global lastTemp
  global temp_stats
  m_decode = str(msg.payload.decode("utf-8"))
  m_in = json.loads(m_decode)
  print(m_in)
  temp_stats = m_in

client = mqtt.Client("temp_counter")

#client.on_log = on_log
client.on_log = on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message

print("Connecting to broker ", broker)
client.username_pw_set(username, password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
client.subscribe("Devices/dht11/temp_stats")
client.publish("Devices", '{"temp_counter": "online"}')
time.sleep(4)

client.loop_start()

try:
  while True:

    sleep(.1)

    

except KeyboardInterrupt:
  pass

except socket.error:
  pass
  print("Error: %s" % e)



client.loop_stop()
client.disconnect()