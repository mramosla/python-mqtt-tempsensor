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

num1 = mqtt_init.notify_num1
num2 = mqtt_init.notify_num2
num3 = mqtt_init.notify_num3
working_mode = mqtt_init.WORKING_MODE

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

def flowroute_loop(text_data):
    print("############################################")
    print("Working Mode: ", working_mode)
    print("flow_testp.py: Sending via flowroute ERROR notification...")
    print("\n")
    recipients = [num1, num2, num3]
    text_data = text_data

    for index, num in enumerate(recipients):     
      print("Outgoing Recipient Index: ", index)
      print("Outgoing Recipient Number: ", num)
      print("Outgoing Data: ", text_data)
      if working_mode == "Prod":
        flow_sms_send(text_data)
      print("\n")


