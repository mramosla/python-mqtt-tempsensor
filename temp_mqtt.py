import time
from time import sleep
from datetime import datetime
import json
import ssl

import paho.mqtt.client as mqtt
import mqtt_init

import Adafruit_DHT

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

last_temp = 0
warn_temp = mqtt_init.warn_temp
dang_temp = mqtt_init.dang_temp

# Temp stats dictionary
temp_stats={
  "tempc":0,
  "tempf":0,
  "humidity":0,
  "temp_status":"Normal"

}

## Covert timestamp to JSON and insert into temp_stats dictionary
temp_stats["timestamp"] = datetime.now()

##### Begin MQTT Settings #####

# Define callbacks
# def on_log(client, userdata, level, buf):
#   print("log: "+buf)

def on_message(client, userdata, msg):
  m_decode = str(msg.payload.decode("utf-8"))
  m_in = json.loads(m_decode)
  print(m_in)

# MQTT local init
client = mqtt.Client("dht11")

#client.on_log = on_log
client.on_message=on_message

print("Connecting to broker ", broker)
client.username_pw_set(username, password)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
client.subscribe("Devices")
client.subscribe("Devices/dht11")
client.subscribe("Devices/dht11/#")
client.publish("Devices", '{"dht11": "online"}')
time.sleep(4)

client.loop_start()

try:
  while True:

      sleep(.1)

      # Define vars capture stats
      humidity, temperature = Adafruit_DHT.read_retry(11, 4)
      tempf = temperature * 9/5 + 32
      timestamp = datetime.now()
      # Add to dict
      temp_stats["tempc"] = temperature
      temp_stats["tempf"] = tempf
      temp_stats["humidity"] = humidity
      temp_stats["timestamp"] = timestamp
      temp_stats["temp_status"] = "Normal"
      if tempf >= warn_temp:
       temp_stats["temp_status"] = "Warning"
      if tempf >= dang_temp:
         temp_stats["temp_status"] = "Danger"


      status = temp_stats["temp_status"]

      # Convert to JSON
      def converter(o):
        if isinstance(o, datetime):
          return o.__str__()

      # Convert to temp_stats to JSON
      json_stats = json.dumps(temp_stats, default = converter)

      
      # If temp F change do:
      if last_temp != tempf:

        # Print stats for temp and humidity w/timestamp
        #print("JSON Stats: {}".format(json_stats))
        client.publish("Devices/dht11/temp_stats",json_stats,qos=0,retain=True)

        last_temp = tempf
        sleep(10)

except KeyboardInterrupt:
  pass

except socket.error:
  pass
  print("Error: %s" % e)

client.loop_stop()
client.disconnect()
