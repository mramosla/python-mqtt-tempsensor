Python scripts to using MQTT to monitor a DHT11 temperature sensor and publish to and oled screen and the web. Alerts are send via text using Twilio. 

If temperature reach certain level the app will send warning message and initiate a server shutdown. 

The server shutdown is run in a different application using a rest api. 

Each script runs as its own process and published data in JSON format. 

Use PM2 or other process manager to run scripts on boot. 

Uses Python3

# Install the following packages
paho-mqtt mysql-connector Flask Flask-MQTT requests twilio

# Setup
Create 2 _init.py files to import settings and password


Example: 

mqtt_init.py

# Setup for MQTT Cloud with SSL but will work with any broker

broker=""
username = ""
password = ""
port = <port number>

# Set URL to rest server
url = ""

# Custom time out options set as needed
timeout = 600
timeout_default = 600

# More custom options
warn_temp = 0

dang_temp = 0

oled_id = ""

FLOWROUTE_USER = ""

FLOWROUTE_KEY = ""

OUTGOING_CID = ""

# twilio_init.py

account_sid = ''
auth_token = ''
twilioNum = ''
sendtoNum = ''

## Files and usage

# temp_mqtt.py 
Monitors temperature sensor and published stats to MQTT in JSON format. 
Stats are published as a retained message. 

Publish Topic: Devices/dht11/temp_stats

# oled_stats.py
Read published temp stats and displays on oled screen. 

Subscribed Topic: Devices/dht11/temp_stats

# temp_counter.py
Performs Logic. 
Temperature has 3 levels "Normal", "Warning", and "Danger".

If temp is at Warning level the app will pause for 10 min, check the temp again and if its still at the warning level it will send a warning text. 

If temp is at the Danger level it will pause for 10 min, check the temp again and if its still in the Danger level it will initiat a server shutdown and send a Shutdown text. 

# twilio_text.py
import into temp_counter.py

This script will send outgoing message thru twilio. 

# app.py
A Flask application to read published temp stats in a web browser.

#  mgtt_mysql.py
Query's Mysql database for recipient First and Last name on outoing text messages.

This file subscribes to MQTT Topic SMS_out/flow.
Query's the recipeints phone number in Mysql and returns the First and Last name. 
This is combined with the the contact details from Topic SMS_out/flow and published to Topic Get_Contact_Name, which is used by the Front End to display Sent Message History. 

# sms_send_2.py 
Handles outgoing text messages and sends thru Twilio or Flowroute. 
