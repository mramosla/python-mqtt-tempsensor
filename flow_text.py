import time
from time import sleep
import datetime
from datetime import datetime
import json
import requests


import paho.mqtt.client as mqtt
import mqtt_init


import ssl

import socket

# Globals
flow_user = mqtt_init.FLOWROUTE_USER
flow_key = mqtt_init.FLOWROUTE_KEY
#caller_id = mqtt_init.OUTGOING_CID

# Send outgoing text using flowroute
def flow_sms_send(data):
  print("sending out flowroute")
  print("Outgoing Text Data: ", data)

  # Covert to json and send out thru flowroute
  data_json = json.dumps(data)
  #client.publish("SMS_out/test", data_json)
  basicAuthCredentials = (flow_user, flow_key)
  URL = "https://api.flowroute.com/v2.1/messages"
  #URL = "http://192.168.2.70:8000/wmqitzwm"
  headers = {'Content-Type': 'application/vnd.api+json'}

  #Flow route send
  r = requests.post(url = URL, headers=headers , auth=basicAuthCredentials, timeout=5, data = data_json)
  if r.status_code == 200:
      print(r.text)
  else:
      print(r.text)