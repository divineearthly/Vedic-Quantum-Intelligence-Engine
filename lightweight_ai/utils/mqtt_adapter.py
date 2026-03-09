import paho.mqtt.client as mqtt
import json
import time

class VQIE_MQTT_Client:
    def __init__(self, broker='broker.hivemq.com', port=1883, topic='vqie/sensors/#'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.latest_packet = None

        # Initialize MQTT Client with the latest API version
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[MQTT] Connected to Broker: {self.broker}")
            client.subscribe(self.topic)
            print(f"[MQTT] Subscribed to: {self.topic}")
        else:
            print(f"[MQTT] Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            self.latest_packet = json.loads(payload)
            print(f"[MQTT] Data received on {msg.topic}")
        except Exception as e:
            print(f"[MQTT] Error parsing payload: {e}")

    def get_packet(self):
        """Returns the latest packet and clears the buffer."""
        packet = self.latest_packet
        self.latest_packet = None
        return packet

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == '__main__':
    print("--- Starting VQIE MQTT Adapter Test ---")
    adapter = VQIE_MQTT_Client()
    adapter.start()

    # Test loop for 5 seconds to check connectivity and retrieval logic
    start_time = time.time()
    try:
        while time.time() - start_time < 5:
            packet = adapter.get_packet()
            if packet:
                print("Latest Packet:", json.dumps(packet, indent=2))
            time.sleep(1)
    finally:
        adapter.stop()
        print("--- MQTT Adapter Test Finished ---")
