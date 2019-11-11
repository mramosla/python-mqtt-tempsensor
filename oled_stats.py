#!/usr/bin/python3
import time
from time import sleep
from datetime import datetime
import json

import paho.mqtt.client as mqtt
import mqtt_init

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import ssl

import socket

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

##### Begin MQTT Settings #####

tempf = 0
tempc = 0
humidity = 0
status = "Normal"

#timestamp = datetime.now()
#print(timestamp)

# Define callbacks
# def on_log(client, userdata, level, buf):
  
#   #print("log: "+buf)

#   timestamp = datetime.now()
  
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
    print("connected OK Returned code = ", rc)
  else:
    print("Bad connection Returned code = ", rc)

def on_disconnect(client, userdata, rc):
  if rc !=0: 
   print("Disconnect: ", rc)

def on_message(client, userdata, msg):
  global tempf
  global tempc
  global humidity
  global status
  m_decode = str(msg.payload.decode("utf-8", "ignore"))
  m_in = json.loads(m_decode)
  #print(m_in)
  #print(type(m_in))
  #print(m_in["tempf"])
  #print(msg.topic)
  #print(type(msg.topic))
  if msg.topic == "Devices/dht11/temp_stats":
    #print(m_in["tempf"])
    tempf = m_in["tempf"]
    tempc = m_in['tempc']
    humidity = m_in["humidity"]
    status = m_in["temp_status"]
    #print(m_in)
    # print(tempf)
    # print(tempc)
    # print(humidity)
    # print(status)

# MQTT local init
client = mqtt.Client(mqtt_init.oled_id, clean_session=False)

#client.on_log = on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message

print("Connecting to broker ", broker)
client.username_pw_set(username, password)
# Comment out if not using SSL/TLS
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect(broker, port) # connect to broker
client.subscribe("Devices", qos=1)
client.subscribe("Devices/oled", qos=1)
client.subscribe("Devices/oled/#", qos=1)
client.subscribe("Devices/dht11/temp_stats", qos=1)
client.publish("Devices", '{"oled": "online"}')
time.sleep(4)

client.loop_start()

##### End MQTT Settings #####

try:
  while True:

      sleep(.1)

    #try:

      # Draw a black filled box to clear the image.
      draw.rectangle((0,0,width,height), outline=0, fill=0)

      # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
      cmd = "hostname -I | cut -d\' \' -f1"
      IP = subprocess.check_output(cmd, shell = True )
      cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
      #CPU = subprocess.check_output(cmd, shell = True )
      #cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
      #MemUsage = subprocess.check_output(cmd, shell = True )
      #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
      #Disk = subprocess.check_output(cmd, shell = True )

      IP2 = (IP.decode('utf-8'))

      # Add MQTT vars
      temp = "Temp: {} F".format(tempf)
      hum = "Humidity: {} %".format(round(humidity))
      status_up = status.upper()
      stat = "Status: {}".format(status_up)

      draw.text((x, top),       "IP: " + str(IP2),  font=font, fill=255)
      draw.text((x, top+8),     str(temp), font=font, fill=255)
      draw.text((x, top+16),    str(hum),  font=font, fill=255)
      draw.text((x, top+25),    str(stat),  font=font, fill=255)

      # Display image.
      disp.image(image)
      disp.display()
      time.sleep(.1)

    # except KeyboardInterrupt:
    #   pass
    #   print("Error...")

except KeyboardInterrupt:
  pass
  disp.clear()
  disp.display()
  print("Keyboard Interupt")

except socket.error:
  pass
  print("Error: %s" % e)

client.loop_stop()
client.disconnect()
   
