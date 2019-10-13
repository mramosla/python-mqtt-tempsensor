from flask import Flask, render_template, jsonify, request
from flask_mqtt import Mqtt
import mqtt_init
import eventlet
import json
from flask_socketio import SocketIO, send
from flask_bootstrap import Bootstrap

# MQTT init settings
broker = mqtt_init.broker
port = mqtt_init.port
username = mqtt_init.username
password = mqtt_init.password


eventlet.monkey_patch()

app = Flask(__name__)

# MQTT Init
app.config['MQTT_BROKER_URL'] = broker
app.config['MQTT_BROKER_PORT'] = port
app.config['MQTT_USERNAME'] = username
app.config['MQTT_PASSWORD'] = password
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_INSECURE'] = True
app.config['MQTT_TLS_CA_CERTS'] = None

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

# Last value variable
last_value = None


@app.route('/')
def index():
  global last_value
  #msg = last_value

  return render_template('index.html')

@app.route('/json_test')
def json_test():

  global last_value  

  return jsonify(last_value)

@socketio.on('message')
def handleMessage(msg):
  print('Message: ' + msg)
  send(msg, broadcast=True)

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('Devices/dht11/temp_stats')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)

    print(data)

    global last_value

    last_value = data




if __name__ == '__main__':
  #app.run(debug=True, host='0.0.0.0')
  socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)