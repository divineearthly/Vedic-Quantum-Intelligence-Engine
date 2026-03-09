import pandas as pd
import time
import json
import os

class SensorStreamAdapter:
    def __init__(self, csv_path, delay=1.0):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV path not found: {csv_path}")
        self.csv_path = csv_path
        self.delay = delay

    def stream_packets(self, limit=None):
        """Generates a stream of sensor data packets from the CSV file."""
        df = pd.read_csv(self.csv_path)
        count = 0
        
        for _, row in df.iterrows():
            if limit and count >= limit:
                break
            
            # Convert row to dictionary (sensor packet)
            packet = row.to_dict()
            yield packet
            
            count += 1
            time.sleep(self.delay)

if __name__ == '__main__':
    # Test block to verify the streaming output format
    DATA_PATH = 'vedic_quantum_intelligence_engine/data/raw/sample_earth_data.csv'
    print(f"--- Initializing Sensor Stream from {DATA_PATH} ---\n")
    
    adapter = SensorStreamAdapter(DATA_PATH, delay=0.5)
    
    try:
        for i, packet in enumerate(adapter.stream_packets(limit=5)):
            print(f"[Packet {i+1}] Emitted:")
            print(json.dumps(packet, indent=2))
            print("-" * 30)
    except Exception as e:
        print(f"Streaming failed: {e}")
