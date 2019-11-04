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
import methods

import time
from time import sleep

# URL To send shutdown command
URL = mqtt_init.url

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

# Set wait period/keepalive
timeout = mqtt_init.timeout
timeout_default = mqtt_init.timeout_default

# Globals

cmd = ''
start_time = 0

## Methods

start_time = 0

def shutdown_counter():
  global cmd
  #print("counter 10 min interval")
  #start_time = datetime.now()
  print("Start Time", start_time)
  print("Waiting: ", timeout)

  curr_time = datetime.now()
  #print("Current Time", curr_time)

  diff = curr_time - start_time
  #print(diff)
  interval = diff.total_seconds()
  print(interval)
  if interval > timeout:
    #print(" ")
    r = requests.get(url = URL, timeout=5)
    if r.status_code == 200:
      print("success")
      print("Send shutdown complete")
      cmd = None
      print("End")

  if cmd == "override":
    return
    
  # elif interval >= 60:
  #   print("1 min")

## End Methods 

# def on_log(client, userdata, level, buf):
  
#   #print("log: "+buf)

#   # Filter out unwanted keepalive logs
#   if buf != "Sending PINGREQ":
#     if buf != "Received PINGRESP":
#       # Print logs to console
#       if level == 1:
#         print('INFO: {}'.format(buf))
#         print('Timestamp: {}\n'.format(timestamp))
#       if level == 2:
#         print('NOTICE: {}'.format(buf))
#         print('Timestamp: {}\n'.format(timestamp))
#       if level == 4:
#         print('WARNING: {}'.format(buf))
#         print('Timestamp: {}\n'.format(timestamp))
#       if level == 8:
#         print('ERROR: {}'.format(buf))
#         print('Timestamp: {}\n'.format(timestamp))
#       if level == 16:
#         print('DEBUG: {}'.format(buf))
#         print('Timestamp: {}\n'.format(timestamp))

def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("connected OK")
  else:
    print("Bad Connection Returned code=", rc)

def on_message(client, userdata, msg):
  m_decode = str(msg.payload.decode("utf-8"))
  print("Message: ", m_decode)
  global cmd
  global start_time
  cmd = m_decode

  if cmd == "shutdown":
    start_time = datetime.now()
    print("Send shutdown start")
  

def on_disconnect(client, userdata, rc):
  if rc !=0: 
   print("Disconnect: ", rc)
          
  

# create client
client = mqtt.Client("temp_counter")

#client.on_log = on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message

print("Connecting to broker ", broker)
client.username_pw_set(username, password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
client.subscribe("Servers/cmd")
client.publish("Devices", '{"shutdown_app": "online"}')
time.sleep(4)

client.loop_start()

try:
  while True:

    sleep(.1)



    if cmd == "shutdown":
      #print("Command: ", cmd)
      shutdown_counter()
    
  


  

    

except KeyboardInterrupt:
  pass

except socket.error:
  pass
  print("Error: %s" % e)



client.loop_stop()
client.disconnect()