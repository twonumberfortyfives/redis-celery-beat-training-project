import asyncio
from gmqtt import Client as MQTTClient
from celery import Celery

# Configure the public MQTT broker and Redis server
MQTT_BROKER = 'broker.emqx.io'
TOPIC = 'sensors/measurements'
REDIS_BROKER = 'redis://redis:6379/0'  # Replace with your Redis URL

# Setup Celery
app = Celery('tasks', broker=REDIS_BROKER)

@app.task
def process_measurement(measurement):
    print(f"Processing measurement: {measurement}")

class MQTTClientHandler:
    def __init__(self):
        self.client = MQTTClient(client_id="test1")
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

    async def connect(self):
        await self.client.connect(MQTT_BROKER)

    async def subscribe(self):
        # Subscribe using the non-async method directly
        self.client.subscribe(TOPIC, 0)

    def on_connect(self, client, flags, rc, properties):
        print(f"Connected with result code: {rc}")
        asyncio.create_task(self.subscribe())  # Create a new task for subscription

    def on_message(self, client, topic, payload, qos, properties):
        payload = payload.decode()
        print(f"Received message on topic {topic}: {payload}")
        process_measurement.delay(payload)

def run_client():
    handler = MQTTClientHandler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.connect())
    loop.run_forever()


if __name__ == "__main__":
    run_client()
