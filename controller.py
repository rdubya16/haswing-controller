import paho.mqtt.client as mqtt
import haswing

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("motor-compass/sensor/heading/state")

def on_heading(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

client = mqtt.Client()

mot = Haswing()

client.on_connect = on_connect

client.message_callback_add("motor-compass/sensor/heading/state", on_heading)

client.connect("localhost", 1883, 60)

client.loop_forever()
