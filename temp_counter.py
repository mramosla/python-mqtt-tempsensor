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

# URL To send shutdown command
URL = "http://165.227.241.194:8301/1p4e9je1"

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
timeout = 20

temp_stats = {
  "tempc": 0,
  "tempf": 0,
  "humidity": 0,
  "temp_status": "Normal",
  "timestamp": ""
}

texts = {
  "warning": "Warning office temp in warning zone",
  "danger": "Warning office temp in danger zone",
  "shutdown": "Office temp in danger zone. Server shutdown sent.",
  "error": "Server not responding. Shutdown failed."
}

##### Begin MQTT Settings #####

# Define callbacks
# def on_log(client, userdata, level, buf):
#   print("log: "+buf)

def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("connected OK")
  else:
    print("Bad Connection Returned code=", rc)

def on_message(client, userdata, msg):
  global lastTemp
  global temp_stats
  m_decode = str(msg.payload.decode("utf-8"))
  m_in = json.loads(m_decode)
  print(m_in)
  temp_stats = m_in

client = mqtt.Client("temp_counter")

#client.on_log = on_log
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

    temp = temp_stats["tempf"]
    status = temp_stats["temp_status"]
    timestamp = temp_stats["timestamp"]

    if status_code == 1:

      if status == "Normal":
        status_code = 0
        print("Reset status code = {}".format(status_code))

    if status != "Normal":

      if status_code == 0:

        print("Temp in {} zone {}".format(status, temp))
        print("Waiting {} sec...".format(timeout))
        print("Timestamp: " + timestamp)
        sleep(timeout)

        print("Checking temp again...\n")
        print("Current temp: {}".format(temp))
        curr_time = str(datetime.now())
        print("Current Time {}".format(curr_time))

        # Update values to current
        temp = temp_stats["tempf"]
        status = temp_stats["temp_status"]
        timestamp = temp_stats["timestamp"]
        
        if status == "Warning":
          print("Temp still in warning zone...\n")
          # Send waring text
          print("Sending warning text...")
          twilio_text.sms_send(status)
          # Set status code = 1
          status_code = 1
          print("Status Code b = {}".format(status_code))

        if status == "Danger":
          print("Critical temp reached sending shutdown...")
          PARAMS = {"message": "shutdown"}
          try:
            r = requests.get(url = URL, timeout=10)
            if r.status_code == 200:
              print("success")
              status_code = 1
              print("Status Code c = {}".format(status_code))
          except:
            pass
            print("Error: Server not responding")
            counter += 1
            if counter == 5:
              print("Server shutown failed 5 times")
              print("sending text")
              status_code = 1
              print("Status Code c1 = {}".format(status_code))

        if status == "Normal":
          print("Temp returned to normal levels")
          status_code = 0
          print("Status Code d = {}".format(status_code))

      lastTemp = temp

except KeyboardInterrupt:
  pass

client.loop_stop()
client.disconnect()