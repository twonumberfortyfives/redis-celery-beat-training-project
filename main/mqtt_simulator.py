import time
import paho.mqtt.client as mqtt
import json
import random

MQTT_BROKER = 'broker.emqx.io'
TOPIC = 'sensors/measurements'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {rc}")

def simulate_measurements():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_BROKER)

    while True:
        measurement = {
            'temperature': round(random.uniform(-10, 40), 2),
            'humidity': round(random.uniform(0, 100), 2),
            'wind_speed': round(random.uniform(0, 20), 2)
        }
        payload = json.dumps(measurement)
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(5)


if __name__ == "__main__":
    simulate_measurements()
