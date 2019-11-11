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

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

# Globals
flow_user = mqtt_init.FLOWROUTE_USER
flow_key = mqtt_init.FLOWROUTE_KEY
caller_id = mqtt_init.OUTGOING_CID

##### Begin MQTT Settings #####

# Define callbacks
# def on_log(client, userdata, level, buf):
#   print("log: "+buf)

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

def on_disconnect(client, userdata, rc):
  if rc !=0: 
   print("Disconnect: ", rc)

def on_message(client, userdata, msg):
    m_decode = str(msg.payload.decode("utf-8"))
    m_in = json.loads(m_decode)
    print(m_in)

    if msg.topic == 'SMS_out/flow':
        data={
            "data": {
                "type": "message",
                "attributes": {
                    "to":m_in["phone"],
                    "from":caller_id,
                    "body":m_in["msg"] 
                }
            }
        }
        print("Data: ", data)
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

    if msg.topic == "SMS_in":
        print("send to twilio")
        print(m_in["message"])
        msg_text = m_in["message"]
        msg_from = m_in["from"]
        message = "Alert: Incoming text from: {}\nMessage: {}".format(msg_from, msg_text)
        print(message)

        # Twilio send
        twilio_text.sms_send(message)

clientID = mqtt_init.sms_send_Id
init_message = { clientID: "online"}

client = mqtt.Client(clientID)


#client.on_log = on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message

print("Connecting to broker ", broker)



client.username_pw_set(username, password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
client.subscribe("SMS_out/flow")
client.subscribe("SMS_out/twilio")
client.subscribe("SMS_test")
client.subscribe("SMS_in")
client.publish("Devices", str(init_message))
time.sleep(4)

client.loop_start()
sleep(0.1)

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