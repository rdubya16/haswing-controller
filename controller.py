import paho.mqtt.client as mqtt
import yaml

with open("conf/controller.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for topic in config['mqtt']['topics'].values():
      client.subscribe(topic)

def on_heading(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

mqtt_host = config['mqtt']['host']
mqtt_port = config['mqtt']['port']

client = mqtt.Client()

client.on_connect = on_connect

boat_compass = config['mqtt']['topics']['compass-boat']
motor_compass = config['mqtt']['topics']['compass-motor']

client.message_callback_add(motor_compass, on_heading)
client.message_callback_add(boat_compass, on_heading)

client.connect(mqtt_host, mqtt_port, 60)

client.loop_forever()
