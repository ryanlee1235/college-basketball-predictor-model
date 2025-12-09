# test_mqtt_server.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✓ Connected with code {rc}")
    client.subscribe("test/rpi")

def on_message(client, userdata, msg):
    print(f"📨 Received: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Starting MQTT test server...")
client.connect("192.0.0.2", 1883, 60)
client.loop_forever()