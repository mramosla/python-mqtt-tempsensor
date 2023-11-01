import time
from time import sleep
import datetime
from datetime import datetime
import json
import requests


import paho.mqtt.client as mqtt
import mqtt_init

import twilio_text
import flow_text
import ssl

import socket

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

# Globals
# flow_user = mqtt_init.FLOWROUTE_USER
# flow_key = mqtt_init.FLOWROUTE_KEY
caller_id = mqtt_init.OUTGOING_CID

num1 = mqtt_init.notify_num1
num2 = mqtt_init.notify_num2

working_mode = mqtt_init.WORKING_MODE

# Print current working mode
print("\n")
print("*********************")
print("\n")
print("WORKING MODE: ", working_mode)
print("\n")
print("*********************")
print("\n")


##### Begin MQTT Settings #####

# Define callbacks
# def on_log(client, userdata, level, buf):
#   print("log: "+buf)

def on_log(client, userdata, level, buf):
  
  #print("log: "+buf)
  
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
    client.subscribe("SMS_out/flow", qos=1)
    client.subscribe("SMS_out/twilio", qos=1)
    client.subscribe("SMS_test", qos=1)
    client.subscribe("SMS_in", qos=1)
  else:
    print("Bad Connection Returned code=", rc)

def on_disconnect(client, userdata, rc):
  if rc !=0: 
   print("Disconnect: ", rc)
   timestamp = datetime.now()
   print("Timestamp: ", timestamp)

def on_message(client, userdata, msg):
  
  try:
    
    error_data={
              "data": {
                  "type": "message",
                  "attributes": {
                      "to":num1,
                      "from":caller_id,
                      "body":"Notification error check web interface." 
                  }
              }
          }
    print("----------------------------------------------------------------")
    print("SMS_in raw - client: ", client)
    print("SMS_in raw - userdata: ", userdata)
    print("SMS_in raw - msg: ", msg)
    m_decode = str(msg.payload.decode("utf-8"))
    print("\n")
    print("m_decode: ", m_decode)
    m_in = json.loads(m_decode)
    print("\n")
    print("----------------------------------------------------------------")
    print("On Message - Incoming MQTT Data: ", m_in)

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

        if working_mode == "Dev":
          print("\n")
          print("SMS_out/flow, Line 111 Dev mode: ", working_mode)
          print("----------------------------------------------------------------")
          print("\n")
          return

        # send outgoing text using flowroute
        if working_mode == "Prod":
          print("\n")
          print("line 118 Executing flow_sms_send function...")
          print("\n")
          flow_text.flow_sms_send(data)
          print("----------------------------------------------------------------")
          print("\n")
        

    # Send outgoing notification text using flowroute
    if msg.topic == "SMS_in":
      print("SMS_in - send to flowroute")
      print("\n")
      print("SMS_in - Whole Message Content: ", m_in)
      msg_text = m_in["message"]
      msg_from = m_in["phone"]
      msg_sender_firstname = m_in["firstname"]
      msg_sender_lastname = m_in["lastname"]
      message = "Alert! Text from: {} {} {}\nMessage: {}".format(msg_sender_firstname, msg_sender_lastname, msg_from, msg_text)
      print("\n")
      print("SMS_in - Send outgoing notification text using flowroute")
      print("SMS_in - line 134 Outgoing notification message: ", message)
      print("----------------------------------------------------------------")
      print("\n")

      # Send notification to these recipients
      recipients = [num1, num2]

      for index, num in enumerate(recipients):
        print("###############################################################")
        #print("Notification Recipient: ", num)


        # Convert to flowroute
        data={
              "data": {
                  "type": "message",
                  "attributes": {
                      "to":num,
                      "from":caller_id,
                      "body":message 
                  }
              }
          }

        
        
        #print("\n")
        print("SMS_in - Data to flowroute: ", data)
        print("\n")

        if working_mode == "Dev":
          #print("\n")
          print("SMS_in - Line 191 Dev mode: ", working_mode)
          print("----------------------------------------------------------------")
          print("Outgoing Recipient Index: ", index)
          print("Outgoing Recipient Number: ", num)
          print("Outboud Notification Data: ", data)
          print("\n")
          print("\n")
          

        if working_mode == "Prod":
          #print("\n")
          print("SMS_in - line 199 Executing flow_sms_send function...")
          print("----------------------------------------------------------------")
          print("Outgoing Recipient Index: ", index)
          print("Outgoing Recipient Number: ", num)
          print("Outgoing Notification Data: ", data)
          print("\n")
          flow_text.flow_sms_send(data)
          print("----------------------------------------------------------------")
          print("\n")
          print("\n")
          
  except Exception as e:
    pass
    print("\n")
    print("ERROR...line 207 on message : ", e)
    print("\n")
    print("Dev Mode: Sending ERROR notification text : ", error_data)
    print("\n")
    # Keep for testing
    if working_mode == "Dev":
      flow_text.flowroute_loop(error_data)
    

    # send outgoing text using flowroute
    if working_mode == "Prod":
      print("\n")
      print("ERROR: line 219 Executing flow_sms_send function...")
      print("ERROR: Sending outgoing notification text.")
      print("\n")
      flow_text.flowroute_loop(error_data)
      print("----------------------------------------------------------------")
      print("\n")


    # Send notification text on incoming messages
    # Commented 8/24/2023 replaced twilio with flowroute for outbound messages
#-------------------------------------------------------------------------------#
    # if msg.topic == "SMS_in":
    #     print("send to twilio")
    #     print("Whole Message Content: ", m_in)
    #     msg_text = m_in["message"]
    #     msg_from = m_in["phone"]
    #     msg_sender_firstname = m_in["firstname"]
    #     msg_sender_lastname = m_in["lastname"]
    #     message = "Alert! Text from: {} {} {}\nMessage: {}".format(msg_sender_firstname, msg_sender_lastname, msg_from, msg_text)
    #     print("Outgoing notification message: ", message)
#-------------------------------------------------------------------------------#

        # Twilio forward to designated recipient

        #twilio_text.sms_send(message)
        #twilio_text.sms_send2(message)

        #twilio_text.sms_send(message)


clientID = mqtt_init.sms_send_Id
init_message = { clientID: "online"}

client = mqtt.Client(clientID)


client.on_log = on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message

print("Connecting to broker ", broker)



client.username_pw_set(username, password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
# client.subscribe("SMS_out/flow", qos=1)
# client.subscribe("SMS_out/twilio", qos=1)
# client.subscribe("SMS_test", qos=1)
# client.subscribe("SMS_in", qos=1)
client.publish("Devices", str(init_message))
time.sleep(4)

client.loop_start()
sleep(0.1)

try:
  while True:

    sleep(.1)

    

except KeyboardInterrupt:
  pass
  client.loop_stop()
  client.disconnect()

except socket.error as e:
  pass
  print("Socket Error: %s", e)



# client.loop_stop()
# client.disconnect()
