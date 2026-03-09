import paho.mqtt.client as mqtt
import json
import time

def publish_scenarios():
    broker = 'broker.hivemq.com'
    port = 1883
    topic = 'vqie/sensors/test'
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    client.connect(broker, port, 60)
    
    scenarios = [
        {
            "name": "Normal Scenario",
            "payload": {
                'timestamp': '2026-03-09 12:00:00', 'temperature': 24.5, 'humidity': 55.0, 
                'air_quality': 40, 'soil_moisture': 0.4, 'light_intensity': 500, 
                'water_level': 10.0, 'vibration_intensity': 0.1, 'precipitation': 5.0, 'NDVI': 0.45
            }
        },
        {
            "name": "High Temperature Scenario",
            "payload": {
                'timestamp': '2026-03-09 12:01:00', 'temperature': 45.0, 'humidity': 30.0, 
                'air_quality': 120, 'soil_moisture': 0.1, 'light_intensity': 850, 
                'water_level': 5.0, 'vibration_intensity': 0.2, 'precipitation': 2.0, 'NDVI': 0.35
            }
        },
        {
            "name": "Critical Water Scenario",
            "payload": {
                'timestamp': '2026-03-09 12:02:00', 'temperature': 18.5, 'humidity': 92.0, 
                'air_quality': 35, 'soil_moisture': 0.95, 'light_intensity': 100, 
                'water_level': 25.0, 'vibration_intensity': 0.7, 'precipitation': 135.0, 'NDVI': 0.82
            }
        }
    ]
    
    print(f"--- Starting VQIE MQTT Stress Test Producer ---")
    for scenario in scenarios:
        print(f"Publishing: {scenario['name']}")
        client.publish(topic, json.dumps(scenario['payload']))
        time.sleep(2) # Give monitor time to process
    
    client.disconnect()
    print("--- Stress Test Publishing Complete ---")

if __name__ == '__main__':
    publish_scenarios()

# Now run the integrated test: Start monitor in background, then run producer
import subprocess
import time

print("\n--- Executing Production Integration Test ---")
# Start the monitor script in the background using a limited iteration count (3 packets)
monitor_proc = subprocess.Popen(['python3', 'vedic_quantum_intelligence_engine/scripts/realtime_monitor.py'], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Wait for monitor to initialize and connect to broker
time.sleep(5)

# Run the producer to send the 3 test packets
subprocess.run(['python3', 'vedic_quantum_intelligence_engine/scripts/mqtt_stress_test_producer.py'])

# Wait for processing and then terminate monitor
time.sleep(10)
monitor_proc.terminate()

# Display the logs from the monitor to verify results
output, _ = monitor_proc.communicate()
print("\n--- Real-Time Monitor Output Logs ---")
print(output)
