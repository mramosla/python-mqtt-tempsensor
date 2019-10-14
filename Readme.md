Python scripts to using MQTT to monitor a DHT11 temperature sensor and publish to and oled screen and the web. Alerts are send via text using Twilio. 

If temperature reach certain level the app will send warning message and initiate a server shutdown. 

The server shutdown is run in a different application using a rest api. 

Each script runs as its own process and published data in JSON format. 

Use PM2 or other process manager to run scripts on boot. 

Uses Python3

# Setup
# Create 2 _init.py files to import settings and password


Example: 

# mqtt_init.py
# setup for MQTT Cloud but will work with any broker

broker=""
username = ""
password = ""
port = <port number>

# Set URL to rest server
url = ""

# Custom time out options set as needed
timeout = 600
timeout_default = 600

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
# import into temp_counter.py

This script will send outgoing message thru twilio. 

# app.py
A Flask application to read published temp stats in a web browser. 
